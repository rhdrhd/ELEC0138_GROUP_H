<script setup>
import { ref, onMounted } from 'vue'
const isDebug = ref(false)

const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const dashboard_api = backend_url + '/dashboard'

const token = localStorage.getItem('userToken');
const resp = ref(null)
const username = ref('')

async function userDashboard() {
    try {
    const response = await fetch(dashboard_api, {
      method: 'POST',
        headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token: token,
      }),
    });
    const data = await response.json();
    resp.value = data
    console.log(data);
    if (response.ok) {
        console.log("get /dashboard response successfully")
        username.value = data.data.user.username
    } else {
      alert(data.msg); // Error or invalid login
    }
    } catch (error) {
    console.error('Error:', error);
    } 
}

onMounted(() => {
    userDashboard();
})
</script>

<template>
  <h1>Dashboard</h1>
  <p>User: {{ username }}</p>
  <div>
    <button @click.prevent="isDebug = !isDebug">
      Debug Mode
    </button> isDebug: {{ isDebug }}
    <div v-if="isDebug">
      Debug info:
      <li>username: {{ username }}</li>
      <li>response: {{ resp }}</li>
      <li>token: {{ token }}</li>
    </div>
  </div>
</template>
