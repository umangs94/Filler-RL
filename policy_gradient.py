import numpy as np
import tensorflow as tf

from filler import FillerEnv


class PolicyGradient:
    def __init__(self, n_episodes, gamma=0.9, update_after_episodes=10, learning_rate=0.01, images_after_episodes=10):
        self.n_episodes = n_episodes
        self.gamma = gamma
        self.update_after_episodes = update_after_episodes
        self.images_after_episodes = images_after_episodes

        self.env = FillerEnv(number_of_colors=8, height=12, width=8)

        self.model = self.create_model()
        self.optimizer = tf.optimizers.Adam(learning_rate=learning_rate)
        self.loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        self.grad_buffer = self.model.trainable_variables
        self.reset_grad_buffer()

    def create_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, input_shape=(self.env.height * self.env.width,), activation='relu'),
            tf.keras.layers.Dense(self.env.number_of_colors, activation='softmax'),
        ])

        model.build()
        print('Model built')

        return model

    def reset_grad_buffer(self):
        for i, grad in enumerate(self.grad_buffer):
            self.grad_buffer[i] = grad * 0

    def get_action_and_grads(self, obs):
        with tf.GradientTape() as tape:
            logits = self.model(obs)
            color_options = self.env.game.get_color_options()

            action_dist = [logits.numpy()[0, c] for c in color_options]
            try:
                action = np.random.choice(color_options, p=action_dist/sum(action_dist))
            except ValueError:
                action = np.random.choice(color_options)
                print(action_dist)
                print(color_options)

            loss = self.loss_fn([action], logits)

        return action, loss, tape.gradient(loss, self.model.trainable_variables)

    def discount_rewards(self, rewards):
        return [sum([r * self.gamma ** j for j, r in enumerate(rewards[i:])]) for i in range(len(rewards))]

    def train(self):
        rewards = []
        losses = []
        for e_n in range(self.n_episodes):
            save_images_suffix = e_n+1 if not e_n % self.images_after_episodes else False
            if save_images_suffix:
                self.model.save('model.h5')

            obs = self.env.reset(save_images_suffix=save_images_suffix)
            e_grads = []
            e_rewards = []
            e_losses = []

            done = False
            while not done:
                action, loss, grads = self.get_action_and_grads(obs)
                obs, reward, done = self.env.step(action)

                e_grads.append(grads)
                e_rewards.append(reward)
                e_losses.append(loss)

            rewards.append(sum(e_rewards))
            losses.append(np.mean(e_losses))
            discounted_rewards = self.discount_rewards(e_rewards)
            rewards_baseline = np.mean(discounted_rewards)

            for grads, reward in zip(e_grads, discounted_rewards - rewards_baseline):
                for i, grad in enumerate(grads):
                    self.grad_buffer[i] += grad * reward

            if not e_n % self.update_after_episodes:
                self.grad_buffer = np.divide(self.grad_buffer, self.update_after_episodes)
                self.optimizer.apply_gradients(zip(self.grad_buffer, self.model.trainable_variables))
                self.reset_grad_buffer()

                print(f'Episode {e_n}\tAverage Reward: {np.mean(rewards[-self.update_after_episodes:])}\t' +
                      f'Average Loss: {np.mean(losses[-self.update_after_episodes:])}')


if __name__ == "__main__":
    P_G = PolicyGradient(n_episodes=100000, update_after_episodes=100, images_after_episodes=10000)
    P_G.train()
    P_G.model.save('model.h5')
    print('Model saved')
