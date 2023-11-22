import express from "express";
import pg from "pg";

const app = express();
const port = 3000;

const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "world",
  password: "1234",
  port: 5432,
});
db.connect();

app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));

async function checkVisited(){
  const result = await db.query("SELECT * FROM visited_countries");

  let countries = [];
  result.rows.forEach((country)=>{
    countries.push(country.country_code);
  });
  return countries;
}


app.get("/", async (req, res) => {
  const countries = await checkVisited();
  res.render('index.ejs',{
    total: countries.length,
    countries: countries,
  });
});

app.post("/add", async (req, res) => {
  const new_country = req.body.country;
  try{
    const result = await db.query("SELECT country_code FROM countries WHERE LOWER(country_name) LIKE '%'||$1||'%'",
    [new_country.toLowerCase()]
    );

    const country_code = result.rows[0].country_code;
    console.log(country_code);
    try{
      await db.query("INSERT INTO visited_countries (country_code) VALUES ($1)",
      [country_code]
      );
      res.redirect('/');
    } catch(err){
      console.log(err);
      const countries = await checkVisited();
      res.render('index.ejs',{
        total: countries.length,
        countries: countries,
        error : "Country has already been added, try again",
      });
    }
  } catch(err){
    console.log(err);
    const countries = await checkVisited();
    res.render('index.ejs',{
      total: countries.length,
      countries: countries,
      error : "Country name does not exist, try again",
    });
  }
});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
