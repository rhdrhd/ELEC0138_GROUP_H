<template>
  <div class="cart-container">
    <h1>Your Cart</h1>
    <div v-if="cartItems.length > 0">
      <ul class="cart-items">
        <li v-for="item in cartItems" :key="item.id" class="cart-item">
          <div class="item-info">
            <h2>{{ item.name }}</h2>
            <p>{{ item.description }}</p>
            <p>Price: ${{ item.price }}</p>
            <p>Quantity: {{ item.quantity }}</p>
          </div>
          <div class="item-actions">
            <button @click="removeItem(item.id)">Remove</button>
          </div>
        </li>
      </ul>
      <div class="cart-total">
        <h2>Total: ${{ totalCost }}</h2>
      </div>
      <div class="cart-total">
        <h2>Your Balance: ${{ getBalance }}</h2>
      </div>
      <div class="cart-topup-checkout-container">
        <button class="cart-top-up" @click="topUp()">Top Up</button>
        <button class="cart-checkout" @click="checkout()">Checkout</button>
      </div>
    </div>
    <div v-else>
      <p>Your cart is empty.</p>
    </div>
  </div>
</template>

<script>
import "@/assets/cart.css"
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'CartView',
  computed: {
    ...mapGetters(['cartItems', 'getBalance']),
    totalCost() {
      console.log(this.cartItems);
      return this.cartItems.reduce((total, item) => {
        const price = Number(item.price);
        const quantity = Number(item.quantity);
        if (!isNaN(price) && !isNaN(quantity)) {
          return total + price * quantity;
        }
        return total;
      }, 0);
    },
  },
  methods: {
    ...mapActions(['removeFromCart']),
    removeItem(itemId) {
      this.removeFromCart(itemId);
    },
    checkout() {
      if (this.getBalance >= this.totalCost) {
        this.$router.push('/payment');
      } else {
        alert("You don't have enough balance! Please top up first.");
      }
    },
    topUp() {
      this.$router.push('/topup');
    }
  },
};
</script>
