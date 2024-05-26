<template>
   <navbar></navbar>
   <div class="container">
       <form @submit.prevent="createBook">
        <h1>{{ sectionName }} Section</h1>
        <h3>Create Book</h3>
           <input class='input-field' placeholder="Name" id="newBook" v-model="newBookName" required />
           <input class='input-field' placeholder="Author" type="text" id="newBook" v-model="newAuthorName"/>
           <input class='input-field' placeholder="Description (Optional)" type="text" id="newBook" v-model="newBookDesc"/>
           <input class='input-field' placeholder="PDF Link" type="text" id="newBook" v-model="newBookPdf" />
           <button class='buttons' type="submit">Create</button>
       </form>
   </div>
   <div>
       <h3>Existing Books</h3>
       <div class="section-container">
       <div class="section-card" v-for="book in books" :key="book.id">
       <h3>{{ book.name }}</h3>
       <a>{{ book.author }}</a><br><br>
       <a>{{ book.description }}</a><br><br>
       <button @click="editBook(book.id, book.name, book.author, book.description, book.pdf)" class="wbuttons">Edit</button>
       <button @click="confirmDelete(book.id)" class="wbuttons">Delete</button>
     </div>
   </div>
   </div>
   <div v-if="editingBook">
       <div class="container">
           <h3>Edit Book</h3>
           <input class='input-field' placeholder ="Name" type="text" id='newBook' v-model="editedBookName" required />
           <input class='input-field' placeholder="Author" type="text" id="newBook" v-model="editedBookAuthor" />
           <input class='input-field' placeholder="Description (Optional)" type="text" id="newBook" v-model="editedBookDesc" />
           <input class='input-field' placeholder="PDF Link" type="text" id="newBook" v-model="editedBookPdf" />
           <button class="buttons" @click="saveEdit">Save</button>
           <button class="buttons" @click="cancelEdit">Cancel</button>
       </div>
   </div>

   <div v-if="confirmingDelete">
       <div>
           <h3>Confirm Delete</h3>
           <p>Are you sure you want to delete this book?</p>
           <button @click="deleteBook" class="buttons">Yes, Delete</button>
           <button @click="cancelDelete" class="buttons">Cancel</button>
       </div>
   </div>
</template>


<script>
import Navbar from './AdminNav.vue';
import axios from 'axios';

export default{
    computed: {
    sectionName() {
        return this.books.length > 0 ? this.books[0].section : '';
    },
},
    components:{
         Navbar
    },
   data(){
       return{
           newBookName:'',
           newAuthorName:'',
           newBookDesc:'',
           sectionId:localStorage.getItem('sectionId'),
           books:[],
           editingBook:null,
           editedBookName:'',
           editedBookAuthor:'',
           editedBookDesc:'',
           confirmingDelete:false,
           deletedBook:'',
           newBookPdf:'',
           editedBookPdf:'',
       };
   },
    mounted(){
        this.fetchBooks();
    },
    methods:{
        fetchBooks(){
            const sectionId = localStorage.getItem('sectionId');
            axios.get(`/books/${sectionId}`)  
                    .then(response => {
                        this.books = response.data;
                    })
                    .catch(error => {
                    console.error(error);
                    });
            },

        async createBook() {
            try {
                const sectionId = localStorage.getItem('sectionId');
                const response = await axios.post(`/books/${sectionId}`, {
                    name: this.newBookName,
                    author: this.newAuthorName,
                    description: this.newBookDesc,
                    pdf: this.newBookPdf,
                });
                if (response && response.data) {
                    console.log(response.data);
                    this.fetchBooks();
                    window.location.reload()
                } else {
                    console.error("Invalid response received from the server.");
                }
            } catch (error) {
                console.error(error.response.data);
            }
        },
        editBook(bookId,bookName,bookAuthor,bookDesc, bookPdf){
            this.editingBook = bookId;
            this.editedBookName = bookName;
            this.editedBookAuthor = bookAuthor;
            this.editedBookDesc = bookDesc;
            this.editedBookPdf = bookPdf;
        },
        saveEdit(){
            axios.put(`/books/edit/${this.editingBook}`,{
                name:this.editedBookName,
                author:this.editedBookAuthor,
                description:this.editedBookDesc,
                pdf:this.editedBookPdf
            })
            .then(response=>{
                console.log(response.data);
                this.fetchBooks();
                this.cancelEdit();

            })

            .catch(error =>{
                console.error(error.response.data);
            });
        },
        cancelEdit(){
            this.editBook= null;
            this.editingBook = false;
            this.editedBookName='';
            this.editedBookAuthor='';
            this.editedBookDesc='';
            this.editedBookPdf='';
            window.location.reload();
        },
        confirmDelete(bookId){
            this.confirmingDelete = true;
            this.deletedBooks = bookId;
        },
        deleteBook() {
            axios.delete(`books/edit/${this.deletedBooks}`)
            .then(response => {
                console.log(response.data);
                this.fetchBooks();
                this.confirmingDelete = null;
            })
            .catch( error=> {
                console.error(error.response.data);
            });
        },
        cancelDelete(){
            this.confirmDelete=null;
            this.confirmingDelete=false;
            this.deletedBook='';
            window.location.reload();
        },
    }
};
</script>