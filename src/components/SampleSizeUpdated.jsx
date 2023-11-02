import React, { useEffect } from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { Checkbox } from '@mui/material'
import { useState } from 'react'
import "./samplesize.css"
import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
import Popup from 'reactjs-popup';
const SampleSizeUpdated = () => {
    const [type,setType] = useState("infinite")
    const [sKnown,setSKnown] = useState(false)
    const [standard_deviation,set_standard_deviation]=useState(null)
    const [conf,set_conf]=useState(false)
    const [population_size,set_population_size] = useState(null)
    const [error,setError]=useState(-1)
    const [confidence_level,set_confidence_level]=useState(0.90)
    const [toggle,setToggle] = useState(false)
    const [buttonClicked,setButtonClicked] = useState(false)
    const [data,setData] = useState({});    
    const [disableButton,setDisableButton] = useState(true)
 const[PopInfoClicked,setPopInfoClicked]=useState(false)
    const[errorInfoClicked,setErrorInfoClicked]=useState(false)
    const[deviationInfoClicked,setDeviationInfoClicked]=useState(false)
    const [confidenceInfoClicked,setConfidenceInfoClicked]=useState(false)
    const handleSubmit =async () => 
{

var data;
if(error < 0 && error > 1 )
{
  alert("Correct Error Inputs!")
}
else if(standard_deviation < 0 && standard_deviation > 1 )
{
  alert("Correct Standard Deviation Inputs!")
}
// else if(error === -1)
// {
//   setDisableButton(true)
// }
else
{
  setDisableButton(true)
setButtonClicked(true)

if(conf){
 data =
    {
    population_size:type === 'finite' ? parseFloat(population_size) : null ,
    error:parseFloat(error),
    standard_deviation: parseFloat(standard_deviation),
    confidence_level : parseFloat(confidence_level)
    }
  }
  else if(!conf)
  {
    data =
    {
    population_size:type === 'finite' ? parseFloat(population_size) : null ,
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
      setDisableButton(false)
    }
    //   console.log(data);
    
  })
  .catch((error) => {
    // Handle any errors that occurred during the request
  });
 
    // }

}
}
 const handleError=(e)=>{
  const es = e.target.value
  if(es < 1 && es >0){ 
  setError(e.target.value)
  setDisableButton(false)
  }
  else   if(es < 0 || es > 1){ 
  setDisableButton(true)
  }
 }
 const handleStandardDeviation=(e)=>{
  const es = e.target.value
  if(es < 1 && es >0){ 
  set_standard_deviation(e.target.value)
  setDisableButton(false)
  }
  else   if(es < 0 || es > 1){ 
  setDisableButton(true)
  }
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
            <select className="form-control"
        id="color"
        name="color"
        // value={type}
        onChange={e=>setType(e.target.value)}
      >

        <option disabled>--select--</option>
        <option value="infinite">Infinite</option>
        <option value="finite">Finite</option>
      </select>
    </td>
  </tr>
  {/* {type === 'finite' &&  */}
  <tr>
    <td>Population Size <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>The total number of individuals or elements in the entire population being studied. It is the entire group from which a  sample is drawn.</div>
                
            </Popup></td>
    <td>
      
      <input disabled={type === "infinite"}  className="form-control" placeholder='Enter N'  onChange={e=>set_population_size(e.target.value)} type='number' />
      
    </td>
  </tr>
  {/* } */}
  <tr>
    <td>Error <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>Imagine you're conducting a survey, and you want to know what percentage of people in your town like ice cream. You survey 500 people and find that 60% of them like ice cream.However, you know that not everyone in your town was surveyed. So, there's a chance that if you surveyed everyone, the percentage might be slightly different.The margin of error is like a safety net around your survey result. It tells you how much your result might vary if you surveyed everyone. If your margin of error is ±5%, it means that the true percentage of people who like ice cream could be as low as 55% or as high as 65%, with 95% confidence.In simple terms, a confidence interval gives you a range of values where you think the true answer lies, and the margin of error tells you how much that range might wiggle if you talked to more people or collected more data. It's a way of being honest about the uncertainty in your estimates.</div>
                
            </Popup></td>
    <td>
        
       <input type='number' required min='0' max="1" className="form-control" placeholder='Error'  onChange={e=>handleError(e)}/>

    </td>
    <td><p>(0.1 - 0.9)<span style={{color:"red"}}>*</span></p></td>
  </tr>
  <tr>
    <td>
    <tr>
      <td>
        Standard Deviation <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>A measure of how much the values in a dataset differ from the mean. It indicates the spread or dispersion of the data points.</div>
                
            </Popup>
      </td>
    <td >
     <Checkbox  style={{}} onChange={e=>setSKnown(!sKnown)}/>
    </td>
    </tr>    
    </td>
    <td>       {sKnown && <>   <input min={0} max={1} className="form-control" placeholder='Enter Standard Deviation' onChange={e=>handleStandardDeviation(e)} type='number'/> </>}</td>
   <td>{sKnown && <p>(0.1 - 0.9)</p>}</td>
  </tr>
  
  <tr>

  <td>
  <tr>
    <td>
      Confidence Level <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>Imagine you're trying to estimate something, like the average height of all students in your school. You can't measure every single student's height; that would take too much time and effort. So, you decide to measure the heights of a sample, say 100 students.Now, here's where the confidence interval comes in. Instead of giving a single number as your estimate (e.g., the average height is 160 cm), you give a range of values (e.g., 155 cm to 165 cm) along with a level of confidence (e.g., 95%).What this means is that you're saying, "I'm 95% confident that the real average height of all students falls between 155 cm and 165 cm based on my sample." In other words, you acknowledge that your estimate might not be perfect, but you're pretty sure it's in that range.</div>
                
            </Popup>
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
    <button onClick={handleSubmit} className="btn btn-primary" disabled={disableButton} >Submit</button>
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

    </div>
    </div>
    </div>
  </div>
  )
}

export default SampleSizeUpdated
