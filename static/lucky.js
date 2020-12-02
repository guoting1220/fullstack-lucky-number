/** processForm: get data from form and make AJAX call to our API. */

async function processForm(evt) {
    evt.preventDefault();

    let name = $("#name").val();
    let year = $("#year").val();
    let email = $("#email").val();
    let color = $("#color").val();

    const response = await axios.post("http://127.0.0.1:5000/api/get-lucky-num", {name, year, email, color});   

    cleanUpTexts();
    handleResponse(response);
}


/** deal with response from our lucky-num API. */
function handleResponse(response) {    
    if (!(response.data.errors)) {
        handleValidResponse(response);
    } 
    else {
        handleErrorResponse(response);
    }    
}

// handle the response with invalid inputs, show the error messages
function handleErrorResponse(resp) {
    errors = resp.data.errors;

    for (let errorKey in errors) {
        $(`#${errorKey}`)
        .next()
        .text(errors[errorKey])
    }
}

// handle the response with valid inputs, show the data fetched from API
function handleValidResponse(resp) {
    const num = resp.data.num.num;
    const numFact = resp.data.num.fact;
    const year = resp.data.year.year;
    const yearFact = resp.data.year.fact;

    $("#lucky-results").html(
        `<p>Your lucky number is ${num}. ${numFact}</p>
         <p>Your birth year (${year}) fact is: ${yearFact}.</p>`
    );
}


// clean up the text areas before new submit
function cleanUpTexts() {
    $("#lucky-results").text("");
    $("#lucky-form").find("b").text("");
}

// add event listener to the form 
$("#lucky-form").on("submit", processForm);
