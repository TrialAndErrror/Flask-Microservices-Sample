import {Panel, Table} from "rsuite";
import {DataType} from "./types";
import {MobileDataType} from "./types";


const MobileTable = ({data}: { data: MobileDataType[] }) => {

    if (data.length === 0) {
        return <p>No Data available!</p>
    }

    return (
        <>
            <Panel header="Temperature Data" bordered className="card-wide bg-dark">
                <Table virtualized data={data} bordered={true}>
                    <Table.Column flexGrow={2} align="center" fixed>
                        <Table.HeaderCell>Output Volume</Table.HeaderCell>
                        <Table.Cell dataKey="volume_and_density"/>
                    </Table.Column>

                    <Table.Column flexGrow={1}>
                        <Table.HeaderCell>Scoops</Table.HeaderCell>
                        <Table.Cell dataKey="scoops"/>
                    </Table.Column>

                    <Table.Column flexGrow={1}>
                        <Table.HeaderCell>Water</Table.HeaderCell>
                        <Table.Cell dataKey="water"/>
                    </Table.Column>
                </Table>
            </Panel>
        </>
    )
}


export {MobileTable as default}