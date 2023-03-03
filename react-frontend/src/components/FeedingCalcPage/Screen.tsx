import {Container, Content, Divider, Panel} from "rsuite";
import useFetch from "react-fetch-hook";
import dayjs from "dayjs";
import {useMediaQuery} from 'react-responsive'

import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone'
import MobileTable from "./mobileTable";
import FullTable from "./fullTable";
import {MobileDataType, DataType} from "./types";
import MobileForm from "./mobileForm";

import createTrigger from "react-use-trigger";
import useTrigger from "react-use-trigger/useTrigger";

const requestTrigger = createTrigger();

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.tz.setDefault("America/New_York")


const FeedingCalcScreen = ({smallSize}: { smallSize: boolean }) => {
    const endpoint = "http://127.0.0.1:55003/data"

    const requestTriggerValue = useTrigger(requestTrigger);
    const {data, isLoading} = useFetch<DataType[]>(endpoint, {depends: [requestTriggerValue]})
    console.log(data)
    if (isLoading) return <Panel header="Loading Feeding Calc Data" bordered className="card-wide bg-light"/>

    if (!data || data.length === 0) {
        return (
            <Container>
                <div className="container">
                    <MobileForm
                        endpoint={endpoint}

                        updateFunc={() => requestTrigger()}
                    />
                </div>
                <div className="container">
                    <Panel header="No Feeding Calculation Data Found!" bordered className="card-wide bg-light">
                        Please wait for data to appear in the database.
                    </Panel>
                </div>
            </Container>
        )
    }

    const mobileData: MobileDataType[] = data.map((entry) => {
        return {
            volume_and_density: `${entry.total_volume} mL @ ${entry.calorie_density} cal`,
            scoops: `${parseFloat(entry.nutramigen_scoops).toFixed(2)}`,
            water: `${parseInt(entry.volume_water)} mL`
        }
    })

    if (smallSize) {
        return (
            <>
                <Container>
                    <div className="container-mobile">
                        <MobileForm
                            endpoint={endpoint}
                            updateFunc={() => requestTrigger()}
                        />
                    </div>
                    <div className="container-mobile">
                        <MobileTable data={mobileData}/>
                    </div>
                </Container>
            </>
        )
    }

    return (
        <>
            <Container>
                <div className="container">

                    <MobileForm
                        endpoint={endpoint}
                        updateFunc={() => requestTrigger()}
                    />
                </div>
                <div className="container">
                    <FullTable data={data}/>
                </div>
            </Container>
        </>
    )
}

export {
    FeedingCalcScreen as
        default
}