import React, { useEffect, useState } from "react";
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box';
import _ from 'lodash';

function InputBar( {setObject, setNewObject } ) {
    

    return (
        <Box>
            <div>
                <TextField
                    id='objectInputBar'
                    label='Object you want to change'
                    onChange={e => setObject(e.target.value)}
                    margin="normal"
                    fullWidth
                    sx={{ width: '98%'}}
                />
            </div>

            <div>
                <TextField
                    id='newObjectInputBar'
                    label='New object you want to replace with'
                    onChange={e => setNewObject(e.target.value)}
                    margin='normal'
                    fullWidth
                    sx={{ width: '98%'}}
                />
            </div>
        </Box>
    )
}

export default InputBar