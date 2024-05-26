<template> 
    <nav class="newnav">
        <div class="name">
            <a @click="goBack" style="cursor: pointer; text-decoration: none; color: inherit;">Go Back</a>
        </div>
    </nav>
    <h1>Search Page</h1>
    <div class="container">
        <input class='input-field' placeholder="Search Here" type="text" v-model="searchQuery"/>
        <button @click="searchBooks" class='buttons' type="submit">Search</button>
    </div>  
    <div v-if="searched"> 
    <div v-if="books.length > 0">
        <table class="tabl">
            <thead>
                <tr>
                <th>Name</th>
                <th>Author</th>
                <th>Section</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="book in books" :key="book.id">
                <td>{{ book.name }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.section }}</td>
                </tr>
            </tbody>
        </table>
    </div> 
    <div v-else>
        <p>No results found</p>
    </div>
    </div>
</template>       

<script>
import axios from 'axios';

export default {
    data() {
        return {
            searchQuery: '',
            books: [],
            searched: false,
        };
    },
    methods: {
        async searchBooks() {
            const access_token = localStorage.getItem('access_token');
            axios.post('/search', { search_query: this.searchQuery }, {
                headers: {
                    Authorization: `Bearer ${access_token}`,
                },
        })
        .then(response => {
          this.books = response.data;
          this.searched = true;
        })
        .catch(error => {
            if (error.response && error.response.data.msg === 'Token has expired') {
                window.location.href = '/login';
            } else {
                console.error(error);
            }
        });
    },
    goBack() {
        this.$router.go(-1);
    }
    },

}
</script>