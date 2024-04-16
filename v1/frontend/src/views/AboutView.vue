<template>
  <div class="container">
    <h1>Welcome to ELEC0138 Project by Group H</h1>
    <p>In this project, a ticket sales website is created. The website is designed to sell tickets for various events. The website has two versions: a safe version and an unsafe version. The safe version is designed to be secure and protect the user's data, while the unsafe version is designed to have vulnerabilities that can be exploited by attackers. The website has various features, including ticket sales, shopping cart, and user reviews. The website is built using Flask for the backend and Vue.js for the frontend. The website uses SQLite as the database.</p>
    
    <section class="features">
  <h2>Key Features</h2>
  <h3>Attacks</h3>
  <ul>
    <li><strong>Phishing: </strong>Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness.</li>
    <li><strong>Brute-force: </strong>Simulate brute-force attacks to test the strength of password policies and authentication methods.</li>
    <li><strong>CSRF (Cross-Site Request Forgery): </strong>Demonstrate how CSRF attacks can manipulate users into performing actions without their knowledge.</li>
    <li><strong>Man-in-the-Middle (MitM): </strong>Analyze the security of communication channels to prevent data interception.</li>
    <li><strong>SQL Injection: </strong>Assess the robustness of database systems against unauthorized data manipulation or access.</li>
    <li><strong>Credential Stuffing: </strong>Highlight the risks of reused credentials and the importance of unique password policies.</li>
    <li><strong>DoS (Denial of Service): </strong>Showcase methods attackers use to disrupt service availability.</li>
    <li><strong>XSS (Cross-Site Scripting): </strong>Explore how malicious scripts can be injected into web pages and compromise user interactions.</li>
  </ul>
  
  <h3>Defense</h3>
  <ul>
    <li><strong>reCAPTCHA: </strong>Enhances security by ensuring interactions are human-driven, preventing automated software attacks.</li>
    <li><strong>Two-factor Authentication: </strong>Strengthens login security by requiring two forms of user verification, dramatically reducing the risk of unauthorized access.</li>
    <li><strong>DoS Defense: </strong>Implements advanced measures to protect against service disruptions caused by Denial of Service attacks.</li>
    <li><strong>JWT (JSON Web Tokens): </strong>Ensures secure user session management through robust token-based authentication.</li>
    <li><strong>XSS Protection: </strong>Provides safeguards against Cross-Site Scripting to maintain the integrity and security of user data.</li>
    <li><strong>Parameterized Database Queries </strong>Protects against SQL injection attacks by separating SQL code from data inputs, ensuring that user inputs cannot alter the structure of SQL queries.</li>
  </ul>
</section>
  </div>
</template>

<script>
import "@/assets/about.css"
</script>
