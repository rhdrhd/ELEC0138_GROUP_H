<template>
  <div class="top-up-container">
    <h1>Top Up Your Account</h1>
    <form @submit.prevent="submitTopUp">
      <div class="form-group">
        <label for="amount">Amount (USD $):</label>
        <input type="number" id="amount" v-model="amount" placeholder="Enter amount" required min="10">
      </div>
      <div class="form-group">
        <label for="cardDetails">Card Details:</label>
        <input type="text" id="cardDetails" v-model="cardDetails" placeholder="Card Number" required>
      </div>
      <button type="submit" :disabled="!isValid">Top Up</button>
    </form>
  </div>
</template>
<script>
export default {
  name: 'TopUp',
  data() {
    return {
      amount: null,
      cardDetails: ''
    };
  },
  computed: {
    isValid() {
      return this.amount >= 10 && this.cardDetails.length > 0;
    }
  },
  methods: {
    async submitTopUp() {
      // Here, implement the logic to process the payment
      console.log('Processing payment for:', this.amount);
      // Normally, you would interact with a payment gateway or API
      alert(`$${this.amount} will be charged to your card.`);
      const username = localStorage.getItem('usernameForVerification');
      const backend_url = import.meta.env.VITE_APP_BACKEND_URL
      const balance_api = backend_url + '/api/v1/balance'
      try {
        const response = await fetch(balance_api, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            username: username,
            balance: this.amount,
          }),
        });
        const data = await response.json();
        if (response.ok) {
          this.$router.push('/dashboard');
        } else {
          alert(data.msg);
        }
      } catch (error) {
        console.error('Top up failed:', error);
        alert('Top up failed. Please try again later.');
      }
      // Reset fields
      this.amount = null;
      this.cardDetails = '';
    }
  }
};
</script>

<style scoped>
.top-up-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="number"],
input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #81D8D0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
}
</style>
