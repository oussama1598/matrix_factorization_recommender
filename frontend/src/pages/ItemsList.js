import React, {useEffect, useState} from "react";
import Book from "../components/Book";
import {CircularProgress, FormControl, Grid, InputLabel, MenuItem, Select, Typography} from "@mui/material";


export default function ItemsList() {
    const [item, setItem] = useState(314);
    const [loading, setLoading] = useState(true);
    const [books, setBooks] = useState([]);

    const loadBooks = async () => {
        const books = await (await fetch(`http://127.0.0.1:9001/api/v1/items/${item}/top`)).json()

        setBooks(books);
        setLoading(false);
    }

    const handleChange = (event) => {
        setItem(event.target.value);

        setLoading(true);
        loadBooks();
    }

    useEffect(() => {
        loadBooks();
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
                                    <MenuItem value={314}>Inkheart (Inkworld, #1)</MenuItem>
                                    <MenuItem value={20}>Mockingjay (The Hunger Games, #3)</MenuItem>
                                    <MenuItem value={30}>Gone Girl</MenuItem>
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