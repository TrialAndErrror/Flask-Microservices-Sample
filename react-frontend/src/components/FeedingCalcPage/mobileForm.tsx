import {Button, ButtonToolbar, Form, Panel} from "rsuite";
import axios from "axios";
import {useState} from "react";

type mobileFormProps = {
    endpoint: string
    updateFunc: Function
}


const mobileForm = ({endpoint, updateFunc}: mobileFormProps) => {
    const [calories, setCalories] = useState('')
    const [volume, setVolume] = useState('')


    async function postData(url = endpoint, data = {
        "command": "feeding_calc",
        "data": {
            "volume": volume,
            "calories": calories,
        }
    }) {
        // Default options are marked with *
        const response = await fetch(endpoint, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, *cors, same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
            },
            redirect: "follow",
            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        }).then(value => {
            console.log(value)
            updateFunc()
        });
    }

    return (
        <Panel header="Temperature Data" bordered className="card-wide bg-dark">
            <Form fluid onSubmit={() => postData()}>
                <Form.Group controlId="name-1">
                    <Form.ControlLabel>Total Volume</Form.ControlLabel>
                    <Form.Control value={volume} onChange={(value) => setVolume(value)} name="volume"/>
                    <Form.HelpText>Required</Form.HelpText>
                </Form.Group>
                <Form.Group controlId="email-1">
                    <Form.ControlLabel>Calories</Form.ControlLabel>
                    <Form.Control value={calories} onChange={(value) => setCalories(value)} name="calories"
                                  type="email"/>
                    <Form.HelpText>Required</Form.HelpText>
                </Form.Group>
                <Form.Group>
                    <ButtonToolbar>
                        <Button appearance="primary" onClick={() => postData()}>Submit</Button>
                        <Button appearance="default" onClick={() => {
                            setVolume('')
                            setCalories('')
                        }
                        }>Cancel</Button>
                    </ButtonToolbar>
                </Form.Group>
            </Form>
        </Panel>
    )
}

export {mobileForm as default}