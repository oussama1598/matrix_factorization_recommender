import React, {useEffect, useState} from "react";
import Book from "../components/Book";
import {CircularProgress, FormControl, Grid, InputLabel, MenuItem, Select, Typography} from "@mui/material";


export default function UserList() {
    const [algorithm, setAlgorithm] = useState('matrix_factorization')
    const [user, setUser] = useState(314);
    const [loading, setLoading] = useState(true);
    const [books, setBooks] = useState([]);

    const loadBooks = async (i, a) => {
        const books = await (await fetch(`http://127.0.0.1:9001/api/v1/${a}/${i}/top/10`)).json()

        setBooks(books);
        setLoading(false);
    }

    const handleChangeAlgorithm = (event) => {
        setAlgorithm(event.target.value);

        setLoading(true);
        loadBooks(user, event.target.value);
    }

    const handleChange = (event) => {
        setUser(event.target.value);

        setLoading(true);
        loadBooks(event.target.value, algorithm);
    }

    useEffect(() => {
        loadBooks(user, algorithm);
    }, []);

    return (
        <div>
            <Grid container direction="column" style={{padding: '20px'}}>
                <Grid item>
                    <Grid container direction="row" justifyContent="space-between"
                          alignItems="center">
                        <Grid item>
                            <Typography variant="h4">Top 10 Recommendations for User ID {user}</Typography>
                        </Grid>
                        <Grid item>
                            <FormControl variant="standard" style={{paddingRight: '20px'}}>
                                <InputLabel id="demo-simple-select-label">Algorithm</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={algorithm}
                                    label="Algorithm"
                                    onChange={handleChangeAlgorithm}
                                    disabled={loading}
                                >
                                    <MenuItem value="matrix_factorization">Matrix Factorization</MenuItem>
                                    <MenuItem value="knn_user">Knn</MenuItem>
                                </Select>
                            </FormControl>
                            <FormControl variant="standard">
                                <InputLabel id="demo-simple-select-label">User</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={user}
                                    label="User"
                                    onChange={handleChange}
                                    disabled={loading}
                                >
                                    <MenuItem value={314}>User 1</MenuItem>
                                    <MenuItem value={20}>User 2</MenuItem>
                                    <MenuItem value={30}>User 3</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item>
                    {!loading ? <Grid container spacing={4} style={{padding: 24}}>
                            {books.map(book => (
                                <Grid item xs={6} sm={4} lg={2} xl={2}>
                                    <Book imageUrl={book.image_url} title={book.title} rating={parseInt(book.rating)}/>
                                </Grid>
                            ))}
                        </Grid> :

                        <Grid container direction="row" justifyContent="center" alignItems="center"
                              style={{"height": "calc(100vh - 64px)"}}>
                            <Grid item>
                                <CircularProgress/>
                            </Grid>
                        </Grid>}
                </Grid>
            </Grid>
        </div>
    );
}