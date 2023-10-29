import React from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { Checkbox } from '@mui/material'
import { useState } from 'react'
import "./samplesize.css"
import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
const SampleSizeUpdated = () => {
    const [type,setType] = useState("select")
    const [sKnown,setSKnown] = useState(false)
    const [standard_deviation,set_standard_deviation]=useState(null)
    const [conf,set_conf]=useState(false)
    const [population_size,set_population_size] = useState(null)
    const [error,setError]=useState(0)
    const [confidence_level,set_confidence_level]=useState(0.90)
    const [toggle,setToggle] = useState(false)
    const [buttonClicked,setButtonClicked] = useState(false)
    const [data,setData] = useState({});    
    const handleSubmit =async () => 
{
 
setButtonClicked(true)

var data;
// if(error === 0 )
// {alert("Correct error field value")
// setButtonClicked(false)
// setToggle(false)}
// else{
if(conf){
 data =
    {
    population_size:type === 'inifinte' ? parseFloat(population_size) : null ,
    error:parseFloat(error),
    standard_deviation: parseFloat(standard_deviation),
    confidence_level : parseFloat(confidence_level)
    }
  }
  else if(!conf)
  {
    data =
    {
    population_size:type === 'inifinte' ? parseFloat(population_size) : null ,
    error:parseFloat(error),
    standard_deviation: parseFloat(standard_deviation),
    }
  }
console.log(data)
 fetch("https://100102.pythonanywhere.com/sample-size/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})

  .then((response) => response.json())
  .then((data) => {
    console.log(data)
    if(data.error)
    {
      alert("Check your inputs!")
      // setToggle(false)

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

// }
}
  return (
    <div>
 <div className='mobile'>
 <h3 style={{textAlign:"center",paddingTop:"1em"}}>Sample Size Experiment</h3>
 <div style={{display:"flex",padding:"1em",justifyContent:"space-between",gap:"5em"}}>
 <div>
 <table>
  <tr>
    <td>Type</td>
    <td>
       <label>
            <input
              type="radio"
              name="color"
              value="infinite"
              // checked={setType === 'infinite'}
              onChange={e=>setType('infinite')}/>
            Infinte 
          </label>
           <label>
            <input
              type="radio"
              name="color"
              value="finite"
              // checked={setType === 'finite'}
              onChange={e=>setType('finite')}
            />
            Finite
          </label>
    </td>
  </tr>
  {type === 'finite' && 
  <tr>
    <td>Population Size</td>
    <td>
      
      <input  class="form-control" placeholder='Enter N'  onChange={e=>set_population_size(e.target.value)} type='number' />
      
    </td>
  </tr>
  }
  <tr>
    <td>Error</td>
    <td>

       <input type='number' required min={0} max={1} className="form-control" placeholder='Error'  onChange={e=>setError(e.target.value)}/>
    </td>
  </tr>
  <tr>
    <td>
    <tr>
      <td>
        Standard Deviation 
      </td>
    <td >
     <Checkbox  style={{}} onChange={e=>setSKnown(!sKnown)}/>
    </td>
    </tr>    
    </td>
    <td>       {sKnown && <>   <input min={0} max={1} class="form-control" placeholder='Enter Standard Deviation' onChange={e=>set_standard_deviation(e.target.value)} type='number'/> </>}</td>
  </tr>
  
  <tr>

  <td>
  <tr>
    <td>
      Confidence Level
    </td>
<td >
   <Checkbox  style={{marginLeft:'0.9em'}} onChange={e=>set_conf(!conf)}/>
</td>
</tr>
  </td>
  <td>
    {
        conf && <>
       
       <select className="form-control " onChange={(e)=>set_confidence_level(e.target.value)}>
        <option disabled>--select--</option>
        <option>0.90</option>
        <option>0.95</option>
        <option>0.99</option>
        </select>
        </>
        }
  </td>
  </tr>
  <tr>
    <button onClick={handleSubmit} className="btn btn-primary" disabled={buttonClicked} >Submit</button>
  </tr>
  
  
</table>
</div>
<div>
            {!toggle  ? 
<h3 >Response will appear here<span style={{color:"red"}}>*</span></h3>
:
 
<>
                    <h2>Response</h2>
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
 {toggle &&
    <>
        <button onClick={e=>window.location.reload("/")} className="btn btn-primary"  >Try Again</button>
    </>
    
    }
    </div>
    </div>
    </div>
  </div>
  )
}

export default SampleSizeUpdated
