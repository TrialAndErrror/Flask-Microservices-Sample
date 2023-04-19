import EntriesTable from "./EntriesTable";
import {Container, Panel} from "rsuite";
import EntriesChart from "./EntriesChart";
import useFetch from "react-fetch-hook";
import {DataType, FormattedDataType} from "./types";
import dayjs from "dayjs";

import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone'
import MobileChart from "./MobileChart";
import MobileTable from "./mobileTable";

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.tz.setDefault("America/New_York")

function formatMobileDate(date: Date): string {
    const time = `${date.getHours()}:${date.getMinutes()}`
    const day = `${date.getMonth() + 1}/${date.getDate()}`
    return `${day} ${time}`
}

type TemperaturescreenProps = {
    smallSize: boolean
}
export const TemperatureScreen = ({smallSize}: TemperaturescreenProps) => {
    const endpoint = "http://127.0.0.1:55004"

    const {data, isLoading} = useFetch<DataType[]>(endpoint)

    if (isLoading) return <Panel header="Loading Temperature Data" bordered className="card-wide bg-light"/>

    if (!data || data.length === 0) {
        return (
            <Container>
                <div className="container">
                    <Panel header="No Temperature Data Found!" bordered className="card-wide bg-light">
                        Please wait for data to appear in the database.
                    </Panel>
                </div>
            </Container>
        )
    }

    const formattedData: FormattedDataType[] = data.map((entry) => {
        const dateObject = dayjs(entry.created_at, {utc: true}).toDate()
        return {
            ...entry,
            created_at: dateObject,
            created_at_string: dateObject.toString(),
            created_at_mobile: formatMobileDate(dateObject)
        }
    })

    if (smallSize) {
        const lastElement = formattedData.slice(-1)[0]
        return (
            <>
                <Container>
                    <div className="container-mobile">
                        <Panel header="Current Data" bordered className="card-wide bg-dark">
                            <div style={{display: "flex"}}>
                                <p style={{
                                    width: "50%",
                                    textAlign: "center",
                                    fontSize: "24px"
                                }}>Temp: <br/>{lastElement.temperature}</p>
                                <p style={{
                                    width: "50%",
                                    textAlign: "center",
                                    fontSize: "24px",
                                    marginTop: 0
                                }}>Humidity: <br/>{lastElement.humidity} %</p>
                            </div>
                        </Panel>
                    </div>
                </Container>
                <Container>
                    <MobileChart data={formattedData}/>
                </Container>
                <Container>
                    <div className="container-mobile">
                        <MobileTable data={formattedData}/>
                    </div>
                </Container>
            </>
        )
    }

    return (
        <>
            <Container>
                <div className="container">
                    <EntriesChart data={formattedData}/>
                </div>
            </Container>
            <Container>
                <div className="container">
                    <EntriesTable data={formattedData}/>
                </div>
            </Container>
        </>
    )
}
