<template>
  <div>
    <h1>Venues</h1>
    <div class="venues-grid"> 
      <div v-for="venue in venues" :key="venue.id" class="venue-card">
        <div class="venue-info">
        <h2>{{ venue.name }}</h2>
        <p>{{ venue.description }}</p>
      </div>
      <div class = "venue-actions">
        <p>Price: ${{ venue.price }}</p>

        <!-- Numeric input for selecting quantity -->

        <input  type="number" v-model.number="venue.quantity" min="1" :max="venue.capacity" />
        <button  @click="addTicketToCart(venue, venue.quantity)">Add to Cart</button>
        </div>
      </div>
  </div>
  </div>
</template>

<script>
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
  },
};
</script>



<style scoped>

/* Add styles for your venues here */
h1 {
  color: #81D8D0;
  padding-top: 5rem;
  margin-bottom: 1rem;
}
h2 {
  font-size: 25px;
  font-style: italic;
}
.venues-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Creates 4 columns */
  gap: 20px; /* Adjusts the space between grid items */
  padding: 20px; /* Adds some padding around the grid */
}

/* Styling for each venue card, remains the same */
.venue-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* This helps to push the button to the bottom */
  border: 1px solid #ccc; /* Example styling */
  padding: 16px;
  border-radius: 8px; /* Example styling */
  background-color: #fff; /* Example styling */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Example styling */
}

.venue-card:hover {
  transform: translateY(-5px); /* Lifts the card slightly on hover */
}

.venue-info {
  padding: 16px;
  flex: 1; /* Allows this div to expand and push actions to the bottom */
}
.venue-actions {
  border-top: 1px solid #ccc; /* Visually separates actions from the rest of the card */
  padding: 16px;
  background: #f9f9f9; /* Slightly different background for the action area */
  display: flex;
  justify-content: space-between; /* Adjust based on your design needs */
  align-items: center;
}

.venue-actions button {
  padding: 8px 16px; /* Example styling */
  background-color: #81D8D0; /* Example styling */
  color: rgb(68, 66, 66); /* Example styling */
  border: none;
  border-radius: 4px; /* Example styling */
  cursor: pointer;
}

.venue-actions button:hover {
  background-color: #9fecec; /* Darken button on hover, example styling */
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .venues-grid {
    grid-template-columns: repeat(3, 1fr); /* Adjust for smaller screens */
  }
}

@media (max-width: 900px) {
  .venues-grid {
    grid-template-columns: repeat(2, 1fr); /* Adjust for even smaller screens */
  }
}

@media (max-width: 600px) {
  .venues-grid {
    grid-template-columns: 1fr; /* Single column for mobile */
  }
}
</style>
