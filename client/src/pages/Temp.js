import { Table, Container, InputGroup, FormControl } from "react-bootstrap";

const Bills = () => {
    return (
        <Container fluid className="bills-page p-4">
            <div className="d-flex flex-row justify-content-between">
                <h2 className="text-light mb-3">All Bills in Congress</h2>
                {/* Search Bar */}
                <div className="search-bar">
                    <InputGroup>
                    <FormControl
                        placeholder="Search"
                        aria-label="Search"
                        aria-describedby="basic-addon1"
                        className="table-search"
                    />
                    </InputGroup>
                </div>
                </div>
            <Table responsive bordered hover variant="dark" className="custom-table">
            <thead>
                <tr>
                <th>Title</th>
                <th>Bill ID</th>
                <th>Type</th>
                <th>Sector</th>
                <th>Rating</th>
                <th>Action Date</th>
                </tr>
            </thead>
            <tbody>
                {/* Sample rows */}
                {Array.from({ length: 20 }).map((_, idx) => (
                <tr key={idx}>
                    <td>Title {idx + 1}</td>
                    <td>B-{1000 + idx}</td>
                    <td>Type {idx + 1}</td>
                    <td>Sector {idx + 1}</td>
                    <td>{Math.floor(Math.random() * 10)}/10</td>
                    <td>{new Date().toLocaleDateString()}</td>
                </tr>
                ))}
            </tbody>
            </Table>  
        </Container>
    );
  };
  
export default Bills;