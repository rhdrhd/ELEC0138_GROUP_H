<template>
  <div class="verify-code-container">
    <h1>Verify Your Email</h1>
    <p class="email-hint">A verification code has been sent to your email: <strong>{{ maskedEmail }}</strong>.</p>
    <input v-model="code" type="text" placeholder="Enter the verification code" @keyup.enter="verifyCode">
    <button @click="verifyCode">Verify</button>
    <button @click="handleReturn" class="return-button">Return to Login</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>


<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const code = ref('');
    const router = useRouter();
    const errorMessage = ref('');
    const email = localStorage.getItem('emailForVerification');

    const maskedEmail = computed(() => {
      if (email) {
        const parts = email.split('@');
        const local = parts[0];
        const maskedLocal = local.length > 3 ? `${local.substring(0, 3)}***` : `${local[0]}**`;
        return `${maskedLocal}@${parts[1]}`;
      }
      return '';
    });

    const verifyCode = async () => {
      if (!code.value) {
        errorMessage.value = 'Please enter the verification code';
        return;
      }
      try {
        const response = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/api/v1/verify-login-code`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, code: code.value }),
        });
        const data = await response.json();
        if (response.ok) {
          localStorage.setItem('isVerified', true);
          router.push('/dashboard');
        } else {
          errorMessage.value = data.msg;
        }
      } catch (error) {
        console.error('Verification failed:', error);
        errorMessage.value = 'Verification failed. Please try again later.';
      }
    };
    
    const handleReturn = () => {
      localStorage.removeItem('userToken');
      localStorage.removeItem('usernameForVerification');
      localStorage.removeItem('emailForVerification');
      localStorage.removeItem('isVerified');

      router.push('/login');
    };

    return {
      code,
      verifyCode,
      errorMessage,
      maskedEmail,
      handleReturn
    };
  }
}
</script>

<style scoped>
.verify-code-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 20px;
}

input,
button {
  margin: 10px;
  padding: 10px;
  width: 300px;
  font-size: 16px;
  border: 1px solid #ccc; /* Add border to match the original button style */
  background-color: #fff; /* Background color */
  color: #333; /* Text color */
  cursor: pointer;
}

button:hover {
  background-color: #f3f4f6; /* Slightly different background on hover */
}

.email-hint {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}

.error-message {
  color: red;
  margin-top: 20px;
}
</style>

