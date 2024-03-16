import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      cart: [],
    };
  },
  mutations: {
    addToCart(state, item) {
      const exists = state.cart.find(product => product.id === item.id);
      if (exists) {
        exists.quantity += 1;
      } else {
        // Ensure the item added to the cart includes the price property
        state.cart.push({...item, quantity: 1});
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