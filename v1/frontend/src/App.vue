<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <header class="headlines">
      <div>
        <nav>
          <RouterLink to="/">
            Home
          </RouterLink>
          <RouterLink to="/cart">
            Cart
          </RouterLink>
          <RouterLink to="/about">
            About
          </RouterLink>
          <RouterLink to="/login">
            Login
          </RouterLink>
        </nav>
      </div>
    </header>
    <RouterView />
  </div>
</template>


<style scoped>
.headlines {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  background-color: #81D8D0;
  /* Change the color as needed */
  z-index: 1000;
  /* Ensures the header stays on top of other content */
  box-shadow: 0 2px 5px rgba(10, 8, 8, 0.2);
  /* Optional: adds a shadow for better visibility */

}

/* Centering the navigation links within the header */
.headlines>div {
  display: flex;
  justify-content: center;
  /* Centers children (nav) horizontally */
  align-items: center;
  /* Centers children vertically (if needed) */
  height: 60px;
  /* Adjust based on your design needs */
  text-decoration: none;
}

nav {
  display: flex;
  gap: 60px;
  /* Adds space between navigation links */
  /* Additional styling as needed */
}

nav a,
nav .router-link-active {
  text-decoration: none;
  color: #66aaa3
    /* Additional styling here */
}

@media (prefers-color-scheme: dark) {
  .headlines {
    background-color: #81D8D0;
  }

  nav a,
  nav .router-link-active {
    text-decoration: none;
    background-color: #81D8D0;
    color: #66aaa3
      /* Additional styling here */
  }
}

.router-link-active {
  color: #fff !important;
  transform: scale(1.4)
}
</style>
