<template>
  <div>
      <navbar></navbar>
      <h1>User Requests</h1>
      <div v-if="requests.length > 0">
        <table class="tabl">
        <thead>
          <tr>
            <th>User ID</th>
            <th>User</th>
            <th>Book ID</th>
            <th>Book</th>
            <th>Accept</th>
            <th>Reject</th>
            <th>Status</th>
            <th>Terminate</th>
          </tr>
        </thead>
        <tbody>
          <tr  v-for="request in requests" :key="request.id">
            <td>{{ request.requested_user }}</td>
            <td>{{ request.user }}</td>
            <td>{{ request.requested_book}}</td>
            <td>{{ request.book }}</td>
            <td><button class="buttons" @click="approveRequest(request.id)">Approve</button></td>
            <td><button class="buttons" @click="rejectRequest(request.id)">Reject</button></td>
            <td>{{ request.approved ? 'Approved' : 'Not Approved' }}</td>
            <td><button class="buttons" @click="deleteRequest(request.id)">Terminate</button></td>
          </tr>
        </tbody>
      </table>
      </div>
      <div v-else>
          <p>No requests pending.</p>
      </div>  
      <h3>Feedback</h3>
      <table class="tabl">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Book ID</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feedback in feedbacks" :key="feedback.id">
            <td>{{ feedback.user_id }}</td>
            <td>{{ feedback.book_id }}</td>
            <td>{{ feedback.feedback }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script>
import axios from 'axios';
import Navbar from './AdminNav.vue';

export default {
  components: {
        Navbar
    },
  data() {
      return {
          requests: [],
          feedbacks: [],
      };
    },

  mounted() {
      this.fetchRequests();
      this.fetchFeedbacks();
  },
  methods: {
    async fetchRequests(){
           axios.get(`/admin/requests`)  
                .then(response => {
                    this.requests = response.data;
                })
                .catch(error => {
                console.error(error);
                });
        },
    approveRequest(id) {
      axios.post(`/admin/requests/${id}`, { approved: true })
        .then(() => {
          this.fetchRequests();
          window.location.reload();
        })
        .catch(error => {
          if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
            }   else {
                    this.errorMessage = 'An error occurred: ' + error.message;
            }
        });
    },
    rejectRequest(id) {
      axios.post(`/admin/requests/${id}`, { approved: false })
        .then(() => {
          this.fetchRequests();
          window.location.reload();
        })
        .catch(error => {
          if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
            }   else {
                    this.errorMessage = 'An error occurred: ' + error.message;
            }
        });
      },    
      deleteRequest(id) {
            axios.delete(`/admin/requests/${id}`)
                .then(response => {
                    console.log(response.data);
                    this.fetchRequests();
                })
                .catch(error => {
                    console.error(error.response.data);
                });
      },
      async fetchFeedbacks(){
        axios.get(`/feedback`)  
            .then(response => {
                this.feedbacks = response.data;
            })
            .catch(error => {
                console.error(error);
            });
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