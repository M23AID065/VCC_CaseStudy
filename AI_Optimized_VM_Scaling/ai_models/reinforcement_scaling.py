import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class QLearningScaler:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            Dense(24, input_dim=self.state_size, activation='relu'),
            Dense(24, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, states, actions, rewards, next_states):
        target = rewards + 0.9 * np.amax(self.model.predict(next_states), axis=1)
        target_full = self.model.predict(states)
        target_full[np.arange(len(actions)), actions] = target
        self.model.fit(states, target_full, epochs=10, verbose=0)

    def predict_action(self, state):
        return np.argmax(self.model.predict(state))

# Example Usage
scaler = QLearningScaler(state_size=3, action_size=3)  # CPU, Memory, Network as states
sample_state = np.array([[0.5, 0.6, 0.4]])  # Example input
action = scaler.predict_action(sample_state)
print("Suggested Scaling Action:", action)
