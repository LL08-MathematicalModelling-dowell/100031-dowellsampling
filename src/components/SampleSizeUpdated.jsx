import React from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { Checkbox } from '@mui/material'
import { useState } from 'react'
import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
const SampleSizeUpdated = () => {
    const [type,setType] = useState("select")
    const [sKnown,setSKnown] = useState(false)
    const [standard_deviation,set_standard_deviation]=useState(null)
    const [population_size,set_population_size] = useState(null)
    const [error,setError]=useState(0.5)
    const [confidence_level,set_confidence_level]=useState(0.90)
    const [toggle,setToggle] = useState(false)
    const [buttonClicked,setButtonClicked] = useState(false)
    const [data,setData] = useState({});    
    const handleSubmit =async () => 
{
 
setButtonClicked(true)
var data =
    {
    population_size,
    error,
    standard_deviation,
    confidence_level 
    }
// console.log(data)
 fetch("https://100102.pythonanywhere.com/sample-size/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})

  .then((response) => response.json())
  .then((data) => {
    if(data.error)
    {
      alert("Check your inputs!")
    }
    else
    {

      setData(data)
      setToggle(true)
      setButtonClicked(false)
    }
    //   console.log(data);
    
  })
  .catch((error) => {
    // Handle any errors that occurred during the request
  });
 
    // }

}

  return (
    <div>
        <div style={{display:"block",justifyContent:"center",marginTop:"5em",gap:"0.5em",width:"70%",marginLeft:"10em"}}>
         <h1 >Sample Size</h1>
         <p>Type:</p>
    <select className="form-control form-control-lg" onChange={e=>setType(e.target.value)}>
        <option value="select">--select--</option>
        <option value="finite">Finite Population</option>
        <option value="infinite">Infinite Population</option>
    </select>
        <div style={{display:"flex",justifyContent:"space-between"}}>
            <div style={{width:"50%",display:"grid",gap:"1em"}}>
                { type !== "select" &&
                <>
                {type === "finite" &&
                <>
                    <label className="form-label">Population Size</label>
      <input  class="form-control" placeholder='Enter N' onChange={e=>set_population_size(e.target.value)} type='number' />
      </> }
        <div style={{display:"flex"}}> 
         <label>Standard Deviation:</label>
        <Checkbox   onChange={e=>setSKnown(!sKnown)}/>
        </div>
            {
                sKnown &&
                <input class="form-control" placeholder='Enter Standard Deviation' onChange={e=>set_standard_deviation(e.target.value)} type='number'/>}
      <label className="form-label">Error</label>
       <input type='number' className="form-control form-control-lg" placeholder='Error'  style={{width:"200px"}}/>
       <select className="form-control form-control-lg" onChange={(e)=>set_confidence_level(e.target.value)}>
        <option disabled>--select--</option>
        <option>0.90</option>
        <option>0.95</option>
        <option>0.99</option>
        </select>
        <button onClick={handleSubmit} className="btn btn-primary">Submit</button>
  </>
  }     
       </div>
            <div style={{width:"50%"}}>
                {toggle  && 
 
<>
                    <h2 style={{marginTop:"2em",display:"grid",justifyContent:"center"}}>Response</h2>
  <Table className="styled-table">
          <TableHead>
            <TableRow >
              <TableCell style={{fontWeight:"bolder"}}>Sample Size</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Process Time</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Method Used</TableCell>
              {/* Add more TableCell elements for additional columns */}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{data.sample_size}</TableCell>
              <TableCell>{data.process_time}</TableCell>
              <TableCell>{data.method_used}</TableCell>
              {/* Add more TableCell elements for additional columns */}
            </TableRow>
          </TableBody>
          </Table>
</>
}
            </div>
        </div>
        {!toggle && buttonClicked &&
 
     <div style={{marginLeft:"30%",justifyContent:"center"}}> 
      <ClipLoader
        color="green"
        loading={true}
        size={50}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      </div>
 
 }
        </div>
      
    </div>
  )
}

export default SampleSizeUpdated
