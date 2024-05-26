<template>
    <div>
    <navbar></navbar>
    <div>
            <h2>Welcome to the World of Reading</h2>
            <p v-if="errorMessage" class="error" style="color: red;">{{ errorMessage }}</p>
    </div>
    <table class="tabl">
      <thead>
        <tr>
          <th>Name</th>
          <th>Author</th>
          <th>Section</th>
          <th>Description</th>
          <th>Request</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.name }}</td>
          <td>{{ book.author }}</td>
          <td>{{ book.section }}</td>
          <td>{{ book.description }}</td>
          <td>
                <a v-if="book.requested === 'pending'" disabled>Requested</a>
                <button v-else @click="requestBook(book.id)" class="buttons">Request</button>
          </td>

        </tr>
      </tbody>
    </table>
    </div>
</template>

<script>
import axios from 'axios';
import Navbar from './UserNav.vue';

export default{
    components: {
        Navbar
    },
    data(){
        return{
            books:[],
            user_id: null,
            errorMessage: null,
        };
    },
    computed:{
        isAdmin(){
            return this.userRole =='admin';
        }
    },
    mounted(){
       this.fetchBooks();
       this.user_id = localStorage.getItem('user_id');
    },
    methods:{
        async fetchBooks(){
           axios.get(`/books`)  
                .then(response => {
                    this.books = response.data;
                })
                .catch(error => {
                console.error(error);
                });
        },
        requestBook(id){
            const access_token = localStorage.getItem('access_token');
            axios.post(`/users/${id}/requests`,{book_id:id, user_id: this.user_id},{
                headers:{
                    Authorization: `Bearer ${access_token}`,
                },
            })
            .then(() => {
                const book = this.books.find(book => book.id === id);
                if (book) {
                    book.requested = 'pending';
                }
            })
            .catch(error => {
                if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
            }   else {
                    this.errorMessage = 'You can only request 5 books at once.';
            }
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

