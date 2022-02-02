import React, {useEffect, useState} from "react";
import Book from "../components/Book";
import {CircularProgress, FormControl, Grid, InputLabel, MenuItem, Select, Typography} from "@mui/material";


export default function ItemsList() {
    const [algorithm, setAlgorithm] = useState('knn_item')
    const [item, setItem] = useState(10);
    const [loading, setLoading] = useState(true);
    const [books, setBooks] = useState([]);

    const loadBooks = async (i, a) => {
        const books = await (await fetch(`http://oussama-pc.local:9001/api/v1/${a}/${i}/top/10`)).json()

        setBooks(books);
        setLoading(false);
    }

    const handleChangeAlgorithm = (event) => {
        setAlgorithm(event.target.value);

        setLoading(true);
        loadBooks(item, event.target.value);
    }

    const handleChange = (event) => {
        setItem(event.target.value);

        setLoading(true);
        loadBooks(event.target.value, algorithm);
    }

    useEffect(() => {
        loadBooks(item, algorithm);
    }, []);

    return (
        <div>
            <Grid container direction="column" style={{padding: '20px'}}>
                <Grid item>
                    <Grid container direction="row" justifyContent="space-between"
                          alignItems="center">
                        <Grid item>
                            <Typography variant="h4">Top 10 Recommendations for Book ID {item}</Typography>
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
                                    <MenuItem value="knn_item">Knn Item</MenuItem>
                                    <MenuItem value="knn_content">Knn Content</MenuItem>
                                </Select>
                            </FormControl>
                            <FormControl variant="standard">
                                <InputLabel id="demo-simple-select-label">Book</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={item}
                                    label="Book"
                                    onChange={handleChange}
                                    disabled={loading}
                                >
                                    <MenuItem value={10}>Pride and Prejudice</MenuItem>
                                    <MenuItem value={30}>Gone Girl</MenuItem>
                                    <MenuItem value={50}>Where the Sidewalk Ends</MenuItem>
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