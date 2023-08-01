extern crate redis;
extern crate serde;
extern crate serde_json;
use redis::Commands;

use octocrab::{Octocrab, params::repos::Commitish};
use hyper::body::to_bytes;
use std::collections::HashMap;

#[macro_use] extern crate serde_derive;

#[derive(Serialize)]
struct Repo {
    name: String,
    description: Option<String>,
    readme: Option<String>,
    homepage: Option<String>,
    url: String,
    stars: u32
}

fn save_repos(repos: HashMap<String, Repo>) -> redis::RedisResult<()> {
    let client = redis::Client::open(
        format!("redis://{}:{}/",
            std::env::var("REDIS_HOST")
                .expect("This application needs the REDIS_HOST variable to be set"),
            std::env::var("REDIS_PORT")
                .expect("This application needs the REDIS_PORT variable to be set"),
            ))?;
    let mut con = client.get_connection()?;

    /* do something here */
    for name in repos.into_iter() {
        let key = format!("miniwebsite:{}", name.0);
        let serialized: String = match serde_json::to_string(&name.1) {
            Ok(data) => data,
            Err(err) => err.to_string()
        };
        con.set(key, serialized)?;
    }

    Ok(())
}

async fn get_data(octocrab: Octocrab, repo_name: String, branch: String) -> String {
    let content: hyper::Response<hyper::Body> = octocrab
        .repos("minigrim0", repo_name)
        .raw_file(Commitish(branch), "README.md")
        .await
        .expect("Failed to get response !");

    let body = content.into_body();
    let truc = match to_bytes(body).await {
        Ok(val) => val,
        Err(_) => panic!("Could fetch bytes")
    };

    // Convert the response body bytes to a string
    String::from_utf8(truc.to_vec()).unwrap()
}

async fn verify_data(response: String) -> bool {
    let parsed = json::parse(response.as_str());
    match parsed {
        Ok(data) => if data["message"] == "No commit found for the ref main" {
            false
        } else {
            false
        },
        Err(_) =>  {
            true
        }
    }
}


#[tokio::main]
async fn main() -> octocrab::Result<()> {
    let token = std::env::var("GITHUB_TOKEN").expect("GITHUB_TOKEN env variable is required");

    let octocrab: Octocrab = Octocrab::builder().personal_token(token).build()?;

    let my_repos = octocrab
        .current()
        .list_repos_for_authenticated_user()
        .type_("owner")
        .sort("updated")
        .per_page(100)
        .send()
        .await?;

    let mut data: HashMap<String, Repo> = HashMap::new();

    for repo in my_repos {
        if repo.private.is_some() && repo.private.unwrap() {
            // If the repo is private, skip it
            continue;
        }

        let body_str: String = get_data(octocrab.clone(), repo.name.clone(), "main".to_string()).await;
        let repo_url: String = match repo.html_url {
            Some(url) => url.to_string(),
            None => "Missing url".to_string()
        };
        let repo_stars: u32 = match repo.stargazers_count {
            Some(amount) => amount,
            None => 0
        };
        
        let readme_str: String;
        match verify_data(body_str.clone()).await {
            false => {
                let readme: String = get_data(octocrab.clone(), repo.name.clone(), "master".to_string()).await;
                if verify_data(readme.clone()).await == true {
                    readme_str = readme;
                } else {
                    readme_str = "No readme found".to_string();
                }
            },
            true =>  {
                readme_str = body_str;
            }
        }

        data.insert(
            repo.name.clone(),
            Repo {
                name: repo.name.clone(),
                description: repo.description,
                readme: Some(readme_str),
                homepage: repo.homepage,
                url: repo_url,
                stars: repo_stars
            }
        );
    }

    save_repos(data).expect("Could not save the repository details");
    Ok(())
}
