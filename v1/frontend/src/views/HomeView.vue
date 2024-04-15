<template>
  <div>
    <h1>Venues</h1>
    <div class="venues-grid">
      <div v-for="venue in venues" :key="venue.id" class="venue-card">
        <div class="venue-info">
          <h2 @click="showDetails(venue)">{{ venue.name }}</h2>
          <p>{{ venue.description }}</p>
        </div>
        <div class="venue-actions">
          <p>Price: ${{ venue.price }}</p>

          <!-- Numeric input for selecting quantity -->

          <input type="number" v-model.number="venue.quantity" placeholder="1" min="2" :max="venue.capacity" />
          <button @click="addTicketToCart(venue, venue.quantity)">Add to Cart</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "@/assets/home.css"
import { useRouter } from 'vue-router';

const router = useRouter();
const backend_url = import.meta.env.VITE_APP_BACKEND_URL
const venues_api = backend_url + '/api/v1/venues'

export default {
  data() {
    return {
      venues: [],
    };
  },
  created() {
    this.fetchVenues();
  },
  methods: {
    async fetchVenues() {
      try {
        const response = await fetch(venues_api);
        if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
        }
        const data = await response.json();
        this.venues = data.data; // Make sure this matches the structure of your response
      } catch (error) {
        console.error("There was an error fetching the venues:", error.message);
      }
    },
    addTicketToCart(venue, quantity) {
      // You might need to initialize quantity if it's not already done
      quantity = quantity || 1; // Default to 1 if no quantity is selected
      if (quantity > venue.capacity) {
        alert('The selected quantity exceeds the available capacity.');
      } else {
        this.$store.dispatch('addToCart', { item: venue, quantityToAdd: quantity });
      }
    },
    showDetails(venue) {
      this.$router.push('/details/' + venue.id);
    },
  },
};
</script>
