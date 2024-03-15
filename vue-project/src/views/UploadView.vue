<template>
  <div  class="container">
    <h2>Upload Word Document</h2>
    <form @submit.prevent="handleUpload" class="upload-form">
      <label for="file">Select file:</label>
      <input type="file" id="file" ref="fileInput" accept=".doc,.docx" />
      <button type="submit">Upload</button>
    </form>
   <!-- Add Student Form -->
    <h2>Add Student</h2>
    <form @submit.prevent="addStudent" class="student-form">
      <label for="firstname">First Name:</label>
      <input type="text" id="firstname" v-model="student.firstname" required />
      <label for="lastname">Last Name:</label>
      <input type="text" id="lastname" v-model="student.lastname" required />
      <label for="emailid">Email ID:</label>
      <input type="text" id="emailid" v-model="student.emailid" required />
      <label for="age">Age:</label>
      <input type="number" id="age" v-model="student.age" required />
      <button type="submit">Submit</button>
    </form>
    </div>
</template>

<script>
export default {
  data() {
    return {
      student: {
        firstname: '',
        lastname:'',
        emailid:'',
        age: null
      }
    };
  },
  methods: {
    handleUpload() {
      const file = this.$refs.fileInput.files[0];

      // Prepare a FormData object for the upload
      const formData = new FormData();
      formData.append("file", file);
      formData.append("TESTS", "this is a string");

      // Log FormData contents to the console
      formData.forEach((value, key) => {
        console.log(`${key}: ${value}`);
      });

      // Sending URL to server side
      fetch("http://127.0.0.1:5000/fill_and_generate_pdf", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle successful upload response from server
          console.log("File uploaded successfully:", data);
        }).then(() => {
          window.alert("File uploaded successfully!")
          window.location.reload();
        })
        .catch((error) => {
          alert("43"+error)
          console.error("Error uploading file:", error);
        });
    },
    addStudent() {

      // 1. Retrieve entered values
    const { firstname, lastname, emailid, age } = this.student;

    // 2. Create student object
    const newStudent = {
        firstname: firstname,
        lastname: lastname,
        emailid: emailid,
        age: age
    };
      // Add student logic
      alert(newStudent.emailid)
      fetch('http://127.0.0.1:5000/insert-student-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newStudent)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add student');
        }
        else
        {
          window.alert("Student Record Inserted successfully!")
          window.location.reload();
        }
        // Handle success response if needed
    })
    .catch(error => {
        console.error('Error adding student:', error.message);
        // Handle error if needed
    });
    }
  },
};
</script>
<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.upload-form,
.student-form {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
