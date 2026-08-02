// Welcome Message
console.log("Student Result Management System Loaded");

// Add Student Validation
function validateStudentForm(){

    let usn = document.forms["studentForm"]["usn"].value;
    let name = document.forms["studentForm"]["name"].value;

    if(usn == "" || name == ""){

        alert("Please fill all fields");

        return false;
    }

    alert("Student Added Successfully");

    return true;
}

// Add Marks Validation
function validateMarksForm(){

    let s1 = document.forms["marksForm"]["subject1"].value;
    let s2 = document.forms["marksForm"]["subject2"].value;
    let s3 = document.forms["marksForm"]["subject3"].value;

    if(s1 > 100 || s2 > 100 || s3 > 100){

        alert("Marks cannot be greater than 100");

        return false;
    }

    alert("Marks Added Successfully");

    return true;
}