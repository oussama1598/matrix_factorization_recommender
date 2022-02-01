import React from "react";
import {Card, CardContent, CardMedia, Rating, Typography} from "@mui/material";

export default function Book({imageUrl, title, rating}) {
    return (
        <div>
            <Card>
                <CardMedia
                    style={{height: 146, paddingTop: "68%"}}
                    image={imageUrl}
                    title={title}
                />

                <CardContent>
                    <Typography variant="h5">
                        {title}
                    </Typography>
                    <Rating name="read-only" value={rating} readOnly/>
                </CardContent>
            </Card>
        </div>
    );
};
