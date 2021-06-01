import './App.css';
import {useState} from "react";
import ApiService from "./ApiService";

function App() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');

    function sendEmail() {
        setError('');
        if (email && validateEmail(email)) {
            ApiService.callPost('/send-email', {email}).then(result => {
                console.log(result);
            }).catch(e => {
                console.log(e);
            })
        } else {
            setError('Invalid emails');
        }
    }

    function handleChanges(e) {
        setEmail(e.target.value)
        setError('')
    }

    function validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    return (
        <div className="main">

            <h3 className="header">Send Email</h3>

            <label className="label" htmlFor="email">Email</label>
            <input type="email" id="email" className={`input ${error && 'invalid-input'}`} name="email"
                   placeholder="Type in your email.."
                   autoComplete="off" value={email} onChange={e => handleChanges(e)}
                   required/>
            {error && <span className="invalid">{error}</span>}

            <input type="submit" onClick={() => sendEmail()} name="submit" value="Log In" className="send-button"/>

        </div>
    );
}

export default App;
