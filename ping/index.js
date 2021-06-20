let express = require('express');
let router = express.Router();
const Redis = require("ioredis");
const sub = new Redis();
const pub = new Redis();

const {v4} = require("uuid");

let ip_to_jobs = {};
let jobs_info = {};

sub.on("message", function(channel, message) {
  message = JSON.parse(message)
  let {ip, ttl, load} = message;
  if (ip_to_jobs[ip])
    ip_to_jobs[ip].forEach((v)=>{
      if (!jobs_info[v])
        jobs_info[v] = {}
      jobs_info[v]["ttl"] = ttl;
      jobs_info[v]["load"] = load;
    });
});

sub.subscribe("ping_result");


const protocols = {
  udp: 17,
  icmp: 1
}

router.get('/', function(req, res, next) {
  res.render("index", {job_token: v4()})
});


router.post('/ping', function(req, res, next) {
  let {ip, job_token, protocol} = req.body;
  if (!ip_to_jobs[ip]) ip_to_jobs[ip] = [];
  ip_to_jobs[ip].push(job_token);
  pub.publish("ping_req", JSON.stringify({ip: ip, protocol: protocol ? protocols[protocol] : 1}));
  res.redirect(`/job/${job_token}`);
});

router.get('/job/:token', function(req, res, next) {
  let {token} = req.params;
  if (!jobs_info[token]) res.json({"message": "not response yet, refresh the page later"})
  else res.json(jobs_info[token])
});

module.exports = router;
