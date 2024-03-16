<template>
  <h1>Login</h1>
  <div>
    <li>Username: <input v-model="username"></li>
    <li>Password: <input v-model="password"></li>
    <button @click.prevent="userLogin" class="login-button">
      Submit
    </button>
  </div>
  <div>
    <button @click.prevent="isDebug = !isDebug" class="login-button">
      Debug Mode
    </button> isDebug: {{ isDebug }}
    <div v-if="isDebug">
      Debug info:
      <li>username: {{ username }}</li>
      <li>password: {{ password }}</li>
      <li>response: {{ resp }}</li>
      <li>token: {{ token }}</li>
    </div>
  </div>
</template>

<script setup>
import "@/assets/login.css"
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const login_api = backend_url + '/api/v1/login'

const username = ref('')
const password = ref('')
const token = ref('')
const isDebug = ref(false)
const resp = ref(null)

async function userLogin() {
  try {
    const response = await fetch(login_api, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });
    const data = await response.json();
    resp.value = data
    console.log(data);
    if (response.ok) {
      token.value = data.data.token
      // We can get it by localStorage.getItem('userToken');
      localStorage.setItem('userToken', token.value);
      // navigate to dashboard after login
      router.push('/dashboard')
    } else {
      alert(data.msg); // Error or invalid login
    }
  } catch (error) {
    // Login failed, remove the token if it exists
    localStorage.removeItem('userToken');
    console.error('Login failed:', error);
  }
}

onMounted(() => {
  if (localStorage.getItem('userToken') !== "") {
    router.push('/dashboard')
  }
})
</script>


