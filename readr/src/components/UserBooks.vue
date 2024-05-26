<template>
    <navbar></navbar>
    <h1>My Books</h1>
    <div>
        <div v-if="issues.length > 0">
            <table class="tabl">
      <thead>
        <tr>
          <th>Book</th>
          <th>Author</th>
          <th>Description</th>
          <th>Date Issued</th>
          <th>Return Date</th>
          <th>Read</th>
          <th>Give Feedback</th>
        </tr>
      </thead>
      <tbody>
        <tr  v-for="issue in issues" :key="issue.id">
          <td>{{ issue.book }}</td>
          <td>{{ issue.author }}</td>
          <td>{{ issue.description}}</td>
          <td>{{ formatDate(issue.date_issued) }}</td>
          <td>{{ formatDate(issue.date_returned) }}</td>
          <td>
            <a v-if="issue.pdf && new Date() <= new Date(issue.date_returned)" class="buttons" :href="issue.pdf" target="_blank">PDF</a>
            <button v-else-if="new Date() > new Date(issue.date_returned)" class="buttons" @click="returnBook(issue.id)">Return</button>
            <span v-else>Unavailable</span>
        </td>
        <td><button class="buttons" @click="feedbackForm(issue.id)">Write</button></td>
        </tr>
      </tbody>
    </table>
        </div>
        <div v-else>
            <p>You have no books.</p>
        </div>
        <div v-if="feedbackFormOpen">
       <div class="container">
           <h3>Feedback Form</h3>
           <input class='input-field' placeholder ="Give your feedback here" type="text" v-model="feedbackText" required />
           <button class="buttons" @click="submitFeedback">Submit</button>
           <button class="buttons" @click="cancelFeedback">Cancel</button>

       </div>
   </div>
    </div>
</template>     

<script>
import Navbar from './UserNav.vue';
import axios from 'axios';

export default {
    components: {
        Navbar
    },
    data() {
        return {
            issues: [],
            user_id: null,
            feedbackFormOpen: false,
            feedbackText: '',                 
        };
    },
    computed:{
        isAdmin(){
            return this.userRole =='admin';
        }
    },
    mounted() {
        this.fetchIssues();
    },
    methods: {
        fetchIssues(){
            const userId = localStorage.getItem('user_id');
            axios.get(`/issued/user/${userId}`)  
            .then(response => {
                this.issues = response.data;
            })
            .catch(error => {
                console.error(error);
            });
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        returnBook(issueId) {
            axios.delete(`/issued/${issueId}`)
                .then(response => {
                    console.log(response.data);
                    this.fetchIssues();
                })
                .catch(error => {
                    console.error(error.response.data);
                });
        },
        feedbackForm(issueId, feedbackText){
            this.feedbackFormOpen = true;
            this.feedbackIssueId = issueId;
            this.feedbackText = feedbackText;
        },
        submitFeedback(){
            axios.post('/feedback',{
                issue_id: this.feedbackIssueId,
                feedback: this.feedbackText
            })
            .then(response => {
                console.log(response.data);
                this.feedbackFormOpen = false;
            })
            .catch(error => {
                console.error(error.response.data);
            });
        },
        cancelFeedback(){
            this.feedbackFormOpen = false;
        },
        logout(){
            const access_token = localStorage.getItem('access_token');
            this.$axios.post('http://127.0.0.1:8000/logout',null,{
                headers:{
                    Authorization: `Bearer ${access_token}`
                }
            })

            .then(()=>{
                localStorage.removeItem('access_token');
                localStorage.removeItem('userRole');
                localStorage.removeItem('user_id');
                localStorage.setItem('isauthenticated',false);
                this.isauthenticated = false;
            })
        },
    },    
};
</script>    