<template>
    <div v-if="venue" class="venue-details">
        <h1 class="venue-name">{{ venue.name }}</h1>
        <div>
            <p class="venue-price">Price: ${{ venue.price }}</p>
            <p class="venue-capacity">Capacity: {{ venue.capacity }}</p>
            <p class="venue-description">Description: {{ venue.description }}</p>
            <p class="venue-location">Location: {{ venue.location }}</p>
        </div>
    </div>
    <div class="user-reviews">
        <h2>User Reviews</h2>
        <div v-if="reviews.length">
            <div v-for="review in reviews" :key="review.id">
                <div class="review">
                    <span class="review-rating"> Rating: {{ review.rating }} stars </span>
                    <p class="review-text"> {{ review.review_text }} </p>
                    <span class="review-date">Reviewed on: {{ review.review_date }} </span>
                </div>
            </div>
        </div>
        <div v-else>
            Sorry, no reviews here.
        </div>
        <div class="review-form">
            <h3 class="add-review-text">Add Your Review</h3>
            <form @submit.prevent="submitReview">
                <label for="reviewText">Review:</label>
                <textarea id="reviewText" v-model="reviewText" placeholder="Enter your review here..."></textarea>
                <label for="rating">Rating:</label>
                <select id="rating" v-model="rating">
                    <option value="">Choose a rating</option>
                    <option value="1">1 - Poor</option>
                    <option value="2">2 - Fair</option>
                    <option value="3">3 - Good</option>
                    <option value="4">4 - Very Good</option>
                    <option value="5">5 - Excellent</option>
                </select>
                <label for="reviewDate">Date:</label>
                <input type="date" id="reviewDate" v-model="reviewDate">
                <button type="submit">Post</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router'

const route = useRoute()
const venueId = ref(null)
const venue = ref(null)
const reviews = ref([])

const rating = ref(null)
const reviewText = ref(null)
const reviewDate = ref(null)

const backend_url = import.meta.env.VITE_APP_BACKEND_URL;
const details_api = `${backend_url}/api/v1/details`;
const review_api = `${backend_url}/api/v1/review`;

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

<style>
.venue-details {
    /* margin: 20px; */
    /* padding: 20px; */
    padding: 16px;
    /* border: 1px solid #ccc; */
    border: 1px solid #81D8D0;
    background-color: #fff;
    border-radius: 8px;
    position: relative;
    justify-content: space-between;
    flex-direction: column;
    display: flex;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

.venue-details:hover {
    transform: translateY(-5px);
}

.venue-name {
    margin-bottom: 10px;
}

.venue-price {
    font-size: 20px;
    color: #81D8D0;
    margin-bottom: 5px;
}

.venue-capacity {
    font-size: 20px;
    color: #81D8D0;
    margin-bottom: 5px;
}

.venue-description {
    font-size: 20px;
    color: #81D8D0;
    margin-bottom: 10px;
}

.venue-location {
    font-size: 16px;
    font-size: 20px;
    color: #81D8D0;
    margin-bottom: 20px;
}

.user-reviews {
    margin-top: 20px;
    margin-bottom: 30px;
}

.review {
    border: 1px solid #81D8D0;
    background-color: #fff;
    padding: 15px;
    margin-bottom: 10px;
    border-left: 5px solid #00ffea;
    border-radius: 4px;
}

.review-rating {
    color: #81D8D0;
}

.review-text {
    font-weight: bold;
    margin-top: 10px;
    font-style: italic;
    color: #81D8D0;
    line-height: 1.5;
}

.review-date {
    font-size: 14px;
    color: rgb(26, 190, 193);
    display: block;
    /* Make date appear on a new line */
    margin-top: 10px;
}

.add-review-text {
    font-weight: bold;
    margin-top: 10px;
    font-style: italic;
    color: #81D8D0;
}

.review-form {
    margin-top: 20px;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #81D8D0;
}

.review-form h3 {
    margin-top: 0;
}

.review-form form {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    margin-top: 10px;
}

.review-form label {
    margin-bottom: 5px;
    color: #81D8D0;
    font-style: italic;
}

.review-form select,
.review-form textarea,
.review-form input[type="date"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.review-form button {
    padding: 10px 15px;
    background: #81D8D0;
    color: #2e2d2d;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.review-form button:hover {
    background-color: #fff;
}

@media (prefers-color-scheme: dark) {
    .venue-details {
        background-color: #2e2d2d;
    }

    .review {
        background-color: #2e2d2d;
    }

    .review-form {
        background-color: #2e2d2d;
    }
}
</style>
