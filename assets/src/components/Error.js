import React from 'react'
import { withStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper'
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'

const styles = theme => ({
  root: {
    flexGrow: 1,
    padding: 8
  }
})

function Error (props) {
  const { classes, children } = props

  const Alert = Button

  return (
    <div className={classes.root}>
      <Alert
        variant="outlined"
        style={{ backgroundColor: "#cce5ff", color: "#004085", borderColor:"#b8daff", width: "100%", padding: 8}}
        disabled
        className={classes.button}
      >
        {children}
      </Alert>
    </div>
  )
}

export default withStyles(styles)(Error)
