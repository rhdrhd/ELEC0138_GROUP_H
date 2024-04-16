<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useStore();

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const balance_api = backend_url + '/api/v1/balance'

const totalCost = computed(() => {
  console.log(store.getters.cartItems);
  return store.getters.cartItems.reduce((total, item) => {
    const price = Number(item.price);
    const quantity = Number(item.quantity);
    if (!isNaN(price) && !isNaN(quantity)) {
      return total + price * quantity;
    }
    return total;
  }, 0);
});

const clearAllCartItems = () => {
  store.dispatch('clearCart');
}

async function checkout() {
  console.log('Checkout now')
  const username = localStorage.getItem('usernameForVerification');
  try {
    const response = await fetch(balance_api, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        username: username,
        balance: -totalCost.value,
      }),
    });
    const data = await response.json();
    if (response.ok) {
      alert("Payment completed!");
      console.info("Clear all items!")
      clearAllCartItems();
      console.info("All items cleared!")
      router.push("/dashboard");
    } else {
      alert("Checkout failed: " + data.msg);
      router.push("/dashboard");
    }
  } catch (error) {
    console.error('Checkout failed:', error);
    alert('Checkout failed. Please try again later.');
    router.push("/dashboard");
  }
}

onMounted(() => {
  checkout();
})
</script>

<template>
  <h1>Thank you very much! </h1>
</template>
