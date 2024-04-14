<template>
    <div v-if="venue">
        <h1>{{ venue.name }}</h1>
        <div>
            <p>Price: {{ venue.price }}</p>
            <p>Description: {{ venue.description }}</p>
            <p>Location: {{ venue.location }}</p>
            <p>Capacity: {{ venue.capacity }}</p>
        </div>
    </div>
    <div>
        <h2>User Reviews</h2>
        <div v-if="reviews">
            <div v-for="review in reviews" :key="review.id">
                <div class="review-body">
                    <p> Rating: {{ review.rating }} </p>
                    <p> Review: {{ review.review_text }} </p>
                    <p> Date: {{ review.review_date }} </p>
                </div>
            </div>
        </div>
        <div v-else>
            Sorry, no reviews here.
        </div>
        <form @submit.prevent="submitReview">
            <label for="review">Your Review:</label>
            <textarea id="review" v-model="reviewText" placeholder="Write your review here..."></textarea>

            <label for="rating">Rating:</label>
            <select id="rating" v-model="rating">
                <option disabled value="">Please select one</option>
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
            </select>

            <label for="reviewDate">Review Date:</label>
            <input type="date" id="reviewDate" v-model="reviewDate">

            <button type="submit">Submit Review</button>
        </form>
    </div>
</template>

<script setup>
import "@/assets/details.css"
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router'

const route = useRoute()
const venueId = ref(null)
const venue = ref(null)
const reviews = ref(null)

const rating = ref(null)
const reviewText = ref(null)
const reviewDate = ref(null)

const backend_url = import.meta.env.VITE_APP_BACKEND_URL;
const details_api = `${backend_url}/api/v1/details`;
const review_api = `${backend_url}/api/v1/review`;
const app_mode = import.meta.env.VITE_APP_MODE;

onBeforeMount(() => {
    console.info("On Details Page")
    // Access the ID and use it
    venueId.value = route.params.id;
    console.log('Venue ID:', venueId.value);
    getDetails();
});

async function submitReview() {
    try {
        console.info("Submit a new review through /review")
        const response = await fetch(review_api, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                venue_id: venueId.value,
                review_text: reviewText.value,
                review_date: reviewDate.value,
                rating: rating.value,
            }),
        });
        const data = await response.json();
        console.info(data)
        if (response.ok) {
            console.info("Review submitted! Refresh now!");
            getDetails();
        } else {
            alert(data.msg); // Error or invalid id
        }
    } catch (error) {
        console.error('Submit a new review through /review failed:', error);
    }
}

async function getDetails() {
    try {
        console.info("Send a request to /details/" + venueId.value)
        const response = await fetch(details_api, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                id: venueId.value,
            }),
        });
        const data = await response.json();
        console.info(data)
        if (response.ok) {
            venue.value = data.data;
            reviews.value = data.data.reviews;
        } else {
            alert(data.msg); // Error or invalid id
        }
    } catch (error) {
        console.error('Get /details/' + venueId.value + ' failed:', error);
    }
}
</script>
