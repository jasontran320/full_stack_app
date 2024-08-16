import React, { useState } from 'react';

export default function ContactForm({ existingContact = {}, updateCallback }) {
    const [firstName, setFirstName] = useState(existingContact.firstName || "");
    const [lastName, setLastName] = useState(existingContact.lastName || "");
    const [email, setEmail] = useState(existingContact.email || "");

    const updating = Object.entries(existingContact).length !== 0;//Tells us if you pass an object with at least 1 entry inside it. This is input ithink?


    const onSubmit = async (e) => {
        e.preventDefault()//prevents refreshing page auto
        const data = {
            firstName, 
            lastName,
            email
        }
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact")//f string in javascript
        const options = { //Specifying the json content you are sending to the api
            method: updating ? "PATCH" : "POST", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)//converts javascript object into valid json object
        }
        const response = await fetch(url, options)//Sends this request to the url and then waits for response
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()//takes in this json response after fetching. Remember it is a 2 part process
            alert(data.message)
        } 
        else {
            updateCallback()//tells app.jsx to close modal for us. Think this is built in method
        }
    }

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="firstName">First Name:</label>
                <input 
                    type="text" 
                    id="firstName" 
                    value={firstName} 
                    onChange={(e)=>{setFirstName(e.target.value)}}
                />
            </div>
            <div>
                <label htmlFor="lastName">Last Name:</label>
                <input 
                    type="text" 
                    id="lastName" 
                    value={lastName} 
                    onChange={(e)=>{setLastName(e.target.value)}}
                        />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input 
                    type="text" 
                    id="email" 
                    value={email} 
                    onChange={(e)=>{setEmail(e.target.value)}}
                />
            </div>
            <button type="submit">{updating? "Update": "Create"}</button>
        </form>
    )
}