<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const backend_url = import.meta.env.VITE_APP_BACKEND_URL;
const login_api = `${backend_url}/api/v1/login`;
const register_api = `${backend_url}/api/v1/register`;
const app_mode = import.meta.env.VITE_APP_MODE;

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const token = ref('');
const isDebug = ref(false);
const resp = ref(null);
const recaptchaToken = ref(null);
const recaptchaId = ref(null);
const mode = ref('login'); // Toggle between 'login' and 'register'

const loadRecaptcha = () => {
  nextTick(() => { // Ensure this is called after DOM updates
    const element = document.getElementById('recaptcha-element');
    try{
      if (recaptchaId.value === null) {
        recaptchaId.value = grecaptcha.render(element, {
          'sitekey': '6Lczk7kpAAAAANd46AiA8tL82izCtQy2MvUA5Oug',
          'callback': (token) => { recaptchaToken.value = token; }
        });
      } else {
        grecaptcha.reset(recaptchaId.value); // Reset before rendering again
        recaptchaId.value = grecaptcha.render(element, {
          'sitekey': '6Lczk7kpAAAAANd46AiA8tL82izCtQy2MvUA5Oug',
          'callback': (token) => { recaptchaToken.value = token; }
        });
      }
    } catch(error) {
      console.log('reCAPTCHA library not loaded at the moment')
    }
  });
}

watch(mode, () => {
  if (recaptchaId.value !== null) {
    grecaptcha.reset(recaptchaId.value); // Ensure it's cleared when mode changes
    recaptchaId.value = null;
  }
  loadRecaptcha();
}, { immediate: true });

const sendLoginCode = async (username) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/api/v1/send-login-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.msg);
    }
  } catch (error) {
    console.error('Error sending login code:', error);
    alert('Failed to send login code: ' + error.message);
  }
}


const userLogin = async () => {
  if (app_mode == "safe") {
    if (!recaptchaToken.value) {
      alert("Please complete the reCAPTCHA to login.");
      return;
    }
  }
  try {
    const response = await fetch(login_api, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        'g-recaptcha-response': recaptchaToken.value
      }),
    });
    const data = await response.json();
    if (response.ok) {
      token.value = data.data.token;
      localStorage.setItem('userToken', token.value);
      localStorage.setItem('usernameForVerification', username.value);  // Store username for sending the login code
      localStorage.setItem('emailForVerification', data.data.email);  // Store email for verification
      await sendLoginCode(username.value);  // Now correctly passing username
      router.push('/verify-code');
    } else {
      alert(data.msg);
    }
  } catch (error) {
    console.error('Login failed:', error);
    alert('Login request failed. Please try again later.');
  }
}

const registerUser = async () => {
  try {
    const response = await fetch(register_api, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        confirmPassword: confirmPassword.value
      }),
    });
    const data = await response.json();
    resp.value = data;
    if (response.ok) {
      alert('Registration successful. Please check your email :3');
      router.push('/login');
    } else {
      alert('Please fill in all the blanks');
    }
  } catch (error) {
    console.error('Registration failed:', error);
    alert('Registration request failed. Please try again later.');
  }
}




onMounted(() => {
  if (app_mode === "safe" && localStorage.getItem('userToken') !== null) {
    router.push('/dashboard');
  }
  loadRecaptcha();
});

onUnmounted(() => {
  if (recaptchaId.value !== null) {
    grecaptcha.reset(recaptchaId.value);
    recaptchaId.value = null;
  }
});
</script>

<template>
  <div class = "form-container">
    <div class="top-padding"></div>
  <div v-if="mode === 'login'">
    <h1>Login</h1>
    <div class="input-container">
      <div class="input-box">
        <input v-model="username" type="text" placeholder="Username">
      </div>
      <div class="input-box">
        <input v-model="password" type="password" placeholder="Password">
      </div>
        <div class="input-box" id="recaptcha-element"></div>
    </div>
    
    <div class="button-container">
      <button @click.prevent="userLogin" class="login-button">Login</button>
      <button @click.prevent="mode = 'register'" class="login-button">Register</button>
    </div>
  </div>
  <div v-else>
    <h1>Register</h1>
    <div class="input-container">
      <div class="input-box"><input v-model="username" type="text" placeholder="Username"></div>
      <div class="input-box"><input v-model="email" type="email" placeholder="Email"></div>
      <div class="input-box"><input v-model="password" type="password" placeholder="Password"></div>
      <div class="input-box"><input v-model="confirmPassword" type="password" placeholder="Confirm Password"></div>
    </div>
    <div class="button-container">
      <button @click.prevent="registerUser" class="login-button">Register</button>
      <button @click.prevent="mode = 'login'" class="login-button">Back</button>
    </div>
  </div>
</div>

</template>

<style scoped>
@import "@/assets/login.css";
</style>
