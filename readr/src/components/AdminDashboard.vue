<template>
    <navbar></navbar>
   <div class="container">
       <form @submit.prevent="createSection">
        <h3>Create Section</h3>
           <input class='input-field' placeholder="Enter Name" type="text" id="newSection" v-model="newSectionName" required />
           <input class='input-field' placeholder="Enter Description (Optional)" type="text" id="newSection" v-model="newSectionDesc" />
           <button class='buttons' type="submit">Create</button>
       </form>
   </div>
   <div>
       <h3>Existing Sections</h3>
       <div class="section-container">
       <div class="section-card" v-for="section in sections" :key="section.id">
       <h3>{{ section.name }}</h3>
       <a>{{ section.description }}</a><br><br>
       <button @click="editSection(section.id,section.name, section.description)" class="wbuttons">Edit</button>
       <button @click="confirmDelete(section.id)" class="wbuttons">Delete</button>
       <button @click="openBooks(section.id)" class="wbuttons">View Books</button>
     </div>
   </div>
   </div>
   <div v-if="editingSection">
       <div class="container">
           <h3>Edit Section</h3>
           <input class='input-field' placeholder ="Name" type="text" id='newSection' v-model="editedSectionName" required />
           <input class='input-field' placeholder="Description (Optional)" type="text" id="newSection" v-model="editedSectionDesc" />
           <button class="buttons" @click="saveEdit">Save</button>
           <button class="buttons" @click="cancelEdit">Cancel</button>
       </div>
   </div>
   <div v-if="confirmingDelete">
       <div>
           <h3>Confirm Delete</h3>
           <p>Are you sure you want to delete this section?</p>
           <button @click="deleteSection" class="buttons">Yes, Delete</button>
           <button @click="cancelDelete" class="buttons">Cancel</button>
       </div>
   </div>
</template>

<script>
import Navbar from './AdminNav.vue';
import axios from 'axios';

export default{
    components:{
         Navbar
    },
   data(){
       return{
           newSectionName:'',
           newSectionDesc:'',
           sections:[],
           editingSection:null,
           editedSectionName:'',
           editedSectionDesc:'',
           confirmingDelete:false,
           deletedSection:'',
       };
   },
   mounted(){
       this.fetchSections();
   },
   methods:{
       async fetchSections(){
           const access_token = localStorage.getItem('access_token')
           try{
               const response = await axios.get('/sections',{
                   headers:{
                       Authorization: `Bearer ${access_token}`
                   }
               });
               this.sections = response.data;
           } catch(error) {
               console.error(error.response.data);
           }
       },

       async createSection(){
           try{
               const response = await axios.post('/sections',{
                   name: this.newSectionName,
                   description: this.newSectionDesc,

               });
               console.log(response.data);
               this.fetchSections();
               window.location.reload()
           } catch(error){
               console.error(error.response.data);
           }
       },

       editSection(sectionId,sectionName,sectionDesc){
           this.editingSection = sectionId;
           this.editedSectionName = sectionName;
           this.editedSectionDesc = sectionDesc;
       },
       saveEdit(){
           axios.put(`/sections/${this.editingSection}`,{
               name:this.editedSectionName,
               description:this.editedSectionDesc,
           })
           .then(response=>{
               console.log(response.data);
               this.fetchSections();
               this.cancelEdit();

           })

           .catch(error =>{
               console.error(error.response.data);
           });
       },
       cancelEdit(){
           this.editSection= null;
           this.editingSection = false;
           this.editedSectionName='';
           this.editedSectionDesc='';
           window.location.reload();
       },
       confirmDelete(sectionId){
           this.confirmingDelete = true;
           this.deletedSections = sectionId;
       },
       deleteSection() {
           axios.delete(`sections/${this.deletedSections}`)
           .then(response => {
               console.log(response.data);
               this.fetchSections();
               this.confirmingDelete = null;
           })
           .catch( error=> {
               console.error(error.response.data);
           });
       },
       cancelDelete(){
           this.confirmDelete=null;
           this.confirmingDelete=false;
           this.deletedSection='';
           window.location.reload();
       },
       openBooks(sectionId){
           localStorage.setItem('sectionId',sectionId);
           this.$router.push('/adminbooks');

       }
    }
};
</script>