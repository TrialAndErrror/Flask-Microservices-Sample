import {Panel, Table} from "rsuite";
import {DataType} from "./types";


const FullTable = ({data}: {data: DataType[]}) => {

    if (data.length === 0) {
        return <p>No Data available!</p>
    }

    return (
        <>
            <Panel header="Temperature Data" bordered className="card-wide bg-dark">
                <Table virtualized data={data} bordered={true}>
                    <Table.Column flexGrow={1} align="center" fixed>
                        <Table.HeaderCell>Output Volume</Table.HeaderCell>
                        <Table.Cell dataKey="total_volume"/>
                    </Table.Column>

                    <Table.Column flexGrow={1}>
                        <Table.HeaderCell>Calories</Table.HeaderCell>
                        <Table.Cell dataKey="calorie_density"/>
                    </Table.Column>

                    <Table.Column flexGrow={1}>
                        <Table.HeaderCell># Scoops</Table.HeaderCell>
                        <Table.Cell dataKey="nutramigen_scoops"/>
                    </Table.Column>
                    <Table.Column flexGrow={1}>
                        <Table.HeaderCell>Input Water</Table.HeaderCell>
                        <Table.Cell dataKey="volume_water"/>
                    </Table.Column>
                </Table>
            </Panel>
        </>
    )
}


export {FullTable as default}