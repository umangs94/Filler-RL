import numpy as np
import tensorflow as tf

from filler import FillerEnv

GAMMA = 0.99


class PolicyGradient:
    def __init__(self, n_episodes, update_after_episodes=10, learning_rate=0.01):
        self.n_episodes = n_episodes
        self.update_after_episodes = update_after_episodes

        self.env = FillerEnv()

        self.model = self.create_model()
        self.optimizer = tf.optimizers.Adam(learning_rate=learning_rate)
        self.loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        self.grad_buffer = self.model.trainable_variables
        self.reset_grad_buffer()

    def create_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, input_shape=(8*12,)),
            tf.keras.layers.Dense(8, activation='softmax'),
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
            action_dist = logits.numpy()
            action = np.random.choice(self.env.game.color_options, p=action_dist[0])

            color_options = self.env.game.get_color_options()
            if action not in color_options:
                action = np.random.choice(color_options)
            loss = self.loss_fn([action], logits)

        return action, tape.gradient(loss, self.model.trainable_variables)

    def discount_rewards(self, rewards):
        return [r * GAMMA**i for i, r in enumerate(rewards)]

    def train(self):
        rewards = []
        for e_n in range(self.n_episodes):
            obs = self.env.reset(save_images_suffix=e_n+1 if not e_n % self.update_after_episodes else False)
            e_grads = []
            e_rewards = []

            done = False
            while not done:
                action, grads = self.get_action_and_grads(obs)
                obs, reward, done = self.env.step(action)
                e_grads.append(grads)
                e_rewards.append(reward)

            rewards.append(sum(e_rewards))
            discounted_rewards = self.discount_rewards(e_rewards)

            for grads, reward in zip(e_grads, discounted_rewards):
                for i, grad in enumerate(grads):
                    self.grad_buffer[i] += grad * reward

            if not e_n % self.update_after_episodes:
                self.optimizer.apply_gradients(zip(self.grad_buffer, self.model.trainable_variables))
                self.reset_grad_buffer()

                print(f'Episode {e_n}\tAverage Reward: {np.mean(rewards[-self.update_after_episodes:])}')


if __name__ == "__main__":
    P_G = PolicyGradient(n_episodes=10000, update_after_episodes=100)
    P_G.train()