<script setup>
import { ref } from 'vue'

const backend_url = 'http://127.0.0.1:5000'
const login_api = backend_url + '/login'

const username = ref('')
const password = ref('')
const token = ref('')
const isDebug = ref(true)
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
      alert(data.msg); // Successful login
    } else {
      alert(data.msg); // Error or invalid login
    }
  } catch (error) {
    console.error('Error:', error);
  }
}
</script>

<template>
    <h1>Login</h1>
    <div>
        <input v-model="username">
        <input v-model="password">
        <button @click.prevent="userLogin">Submit</button>
    </div>
    <div>
    </div>
    <div>
        <button @click.prevent="isDebug = !isDebug">Debug Mode</button>
        <div v-if="isDebug">Debug info:
            <li>username: {{ username }}</li>
            <li>password: {{ password }}</li>
            <li>response: {{ resp }}</li>
            <li>token: {{ token }}</li>
        </div>
    </div>
</template>
