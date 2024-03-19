import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      cart: [],
    };
  },
  mutations: {
    addToCart(state, { item, quantityToAdd }) {
      const existingItem = state.cart.find(cartItem => cartItem.id === item.id);
      if (existingItem) {
        const potentialNewQuantity = existingItem.quantity + quantityToAdd;
        if (potentialNewQuantity > item.capacity) {
          // Handle the case where adding more exceeds capacity
          alert('The number of tickets have reached the all available tickets.');
        } else {
          existingItem.quantity += quantityToAdd;
          alert('Added successfully!'); 
        }
      } else {
        // Check if initial add exceeds capacity
        if (quantityToAdd > item.capacity) {
          alert('The number of tickets have reached the all available tickets.');
        } else {
          // If not exceeding capacity, add new item to cart
          state.cart.push({ ...item, quantity: quantityToAdd });
          alert('Added successfully!'); 
        }
      }
    },
    removeFromCart(state, itemId) {
      const index = state.cart.findIndex(item => item.id === itemId);
      if (index !== -1) {
        state.cart.splice(index, 1);
      }
    },
  },
  actions: {
    addToCart({ commit }, item) {
      commit('addToCart', item);
    },
    removeFromCart({ commit }, itemId) {
      commit('removeFromCart', itemId);
    },
  },
  getters: {
    cartItems(state) {
      return state.cart;
    },
  },
});