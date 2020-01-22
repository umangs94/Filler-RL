import numpy as np
import tensorflow as tf

from filler import FillerEnv


class PolicyGradient:
    def __init__(self, n_episodes, continue_training=False, gamma=0.9, update_after_episodes=10, learning_rate=0.001, images_after_episodes=10):
        self.n_episodes = n_episodes
        self.gamma = gamma
        self.update_after_episodes = update_after_episodes
        self.images_after_episodes = images_after_episodes

        self.env = FillerEnv(number_of_colors=6, height=8, width=5)

        self.model = self.create_model(
            learning_rate=learning_rate) if not continue_training else \
            tf.keras.models.load_model('model.h5', custom_objects={"_value_loss": self._value_loss,
                                                                   "_logits_loss": self._logits_loss})

    def create_model(self, learning_rate):
        array_input = tf.keras.layers.Input(shape=(self.env.height * self.env.width + 2,))
        hidden_layer = tf.keras.layers.Dense(15, activation='relu')(array_input)
        logits = tf.keras.layers.Dense(self.env.number_of_colors)(hidden_layer)
        value = tf.keras.layers.Dense(1)(hidden_layer)

        model = tf.keras.Model(inputs=array_input, outputs=[logits, value])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                      loss=[self._logits_loss, self._value_loss])
        print('Model compiled')

        return model

    @staticmethod
    def _value_loss(returns, values):
        return 0.5*tf.keras.losses.mean_squared_error(returns, values)

    @staticmethod
    def _logits_loss(actions_and_advs, logits):
        actions, advantages = tf.split(actions_and_advs, 2, axis=-1)

        cross_entropy = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        loss = cross_entropy(actions, logits, sample_weight=advantages)

        return loss

    def get_action_and_value(self, obs, random=False):
        logits, value = self.model.predict(obs)

        color_options = self.env.game.get_color_options()
        if random:
            action = np.random.choice(color_options)
        else:
            action_dist = [[tf.gather(tf.squeeze(logits), c) for c in color_options]]
            action = color_options[tf.squeeze(tf.random.categorical(action_dist, num_samples=1))]

        return action, tf.squeeze(value)

    def discount_rewards(self, rewards):
        return [sum([r * self.gamma ** j for j, r in enumerate(rewards[i:])]) for i in range(len(rewards))]

    def train(self, continue_training=0):
        rewards = []
        logit_losses = []
        value_losses = []

        all_actions = []
        all_obs = []
        all_advs = []
        all_d_rewards = []

        for e_n in range(continue_training, self.n_episodes):
            save_images_suffix = e_n+1 if not e_n % self.images_after_episodes else False
            if save_images_suffix:
                self.model.save('model.h5')

            obs = self.env.reset(save_images_suffix=save_images_suffix)
            e_rewards = []
            e_values = []

            done = False
            while not done:
                all_obs.append(obs.reshape(-1))
                action, value = self.get_action_and_value(obs, random=e_n < self.update_after_episodes * 2)
                obs, reward, done = self.env.step(action)

                all_actions.append(action)
                e_values.append(value)
                e_rewards.append(reward)

            rewards.append(sum(e_rewards))
            discounted_rewards = self.discount_rewards(e_rewards)
            advantages = np.subtract(discounted_rewards, e_values)

            all_advs.extend(advantages)
            all_d_rewards.extend(discounted_rewards)

            if not e_n % self.update_after_episodes:
                all_actions = np.array(all_actions)[:, None]
                all_advs = np.array(all_advs)[:, None]
                actions_and_advs = np.concatenate([all_actions, all_advs], axis=-1)
                _, logit_loss, value_loss = self.model.train_on_batch(
                    np.array(all_obs), [actions_and_advs, np.array(all_d_rewards)])
                logit_losses.append(logit_loss)
                value_losses.append(value_loss)

                all_actions = []
                all_obs = []
                all_advs = []
                all_d_rewards = []

                print(f'Episode {e_n}\tAverage Reward: {np.mean(rewards[-self.update_after_episodes:]):.4f}\t' +
                      f'Average Logit Loss: {np.mean(logit_losses[-self.update_after_episodes:]):.4f}\t' +
                      f'Average Value Loss: {np.mean(value_losses[-self.update_after_episodes:]):.4f}')
            elif not e_n % (self.update_after_episodes/5):
                print(f'Episode {e_n}')


if __name__ == "__main__":
    P_G = PolicyGradient(n_episodes=100000, update_after_episodes=100, images_after_episodes=1000)
    P_G.train()
    # P_G = PolicyGradient(n_episodes=1000000, continue_training=True, update_after_episodes=500, images_after_episodes=50000)
    # P_G.train(continue_training=60000)
    P_G.model.save('model.h5')
    print('Model saved')
