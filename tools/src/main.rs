extern crate redis;
extern crate serde;
extern crate serde_json;
use redis::Commands;

use hyper::body::to_bytes;
use octocrab::{params::repos::Commitish, Octocrab};
use std::collections::HashMap;

#[macro_use]
extern crate serde_derive;

/// Represents a GitHub repository with its details.
#[derive(Serialize)]
struct Repo {
    name: String,
    description: Option<String>,
    readme: Option<String>,
    homepage: Option<String>,
    url: String,
    stars: u32,
}

/// Saves the repository information to Redis.
///
/// # Arguments
///
/// * `repos` - A HashMap containing repository names as keys and Repo structs as values.
///
/// # Returns
///
/// A Redis result indicating success or failure.
fn save_repos(repos: HashMap<String, Repo>) -> redis::RedisResult<()> {
    let redis_url = std::env::var("REDIS_URL").unwrap_or("redis://127.0.0.1/".to_string());

    let client = redis::Client::open(redis_url)?;
    let mut con = client.get_connection()?;

    for name in repos.into_iter() {
        let key = format!("miniwebsite:{}", name.0);
        let serialized: String = match serde_json::to_string(&name.1) {
            Ok(data) => data,
            Err(err) => err.to_string(),
        };

        con.set(key, serialized)?;
    }

    Ok(())
}

/// Fetches the content of a file from a GitHub repository.
///
/// # Arguments
///
/// * `octocrab` - An instance of the Octocrab GitHub API client.
/// * `repo_name` - The name of the repository.
/// * `branch` - The branch name to fetch the file from.
///
/// # Returns
///
/// The content of the file as a String.
async fn get_data(octocrab: Octocrab, repo_name: String, branch: String) -> String {
    let content: hyper::Response<hyper::Body> = octocrab
        .repos("minigrim0", repo_name)
        .raw_file(Commitish(branch), "README.md")
        .await
        .expect("Failed to get response !");

    let body = content.into_body();
    let truc = match to_bytes(body).await {
        Ok(val) => val,
        Err(_) => panic!("Could fetch bytes"),
    };

    // Convert the response body bytes to a string
    String::from_utf8(truc.to_vec()).unwrap()
}

/// Verifies if the response is valid JSON.
///
/// # Arguments
///
/// * `response` - The response string to verify.
///
/// # Returns
///
/// `true` if the response is not valid JSON, `false` otherwise.
async fn verify_data(response: String) -> bool {
    let parsed: Result<json::JsonValue, json::Error> = json::parse(response.as_str());
    match parsed {
        Ok(_data) => false,
        Err(_) => true,
    }
}

#[tokio::main]
async fn main() -> octocrab::Result<()> {
    // Fetch GitHub token from environment variable
    let token = std::env::var("GITHUB_TOKEN").expect("GITHUB_TOKEN env variable is required");

    // Initialize Octocrab client with the GitHub token
    let octocrab: Octocrab = Octocrab::builder().personal_token(token).build()?;

    // Fetch repositories for the authenticated user
    let my_repos = octocrab
        .current()
        .list_repos_for_authenticated_user()
        .type_("owner")
        .sort("updated")
        .per_page(100)
        .send()
        .await?;

    let mut data: HashMap<String, Repo> = HashMap::new();

    // Iterate through repositories and collect data
    for repo in my_repos {
        // Skip private repositories
        if repo.private.is_some() && repo.private.unwrap() {
            continue;
        }

        // Fetch README content
        let body_str: String =
            get_data(octocrab.clone(), repo.name.clone(), "main".to_string()).await;
        
        // Get repository URL
        let repo_url: String = match repo.html_url {
            Some(url) => url.to_string(),
            None => "Missing url".to_string(),
        };
        
        // Get star count
        let repo_stars: u32 = match repo.stargazers_count {
            Some(amount) => amount,
            None => 0,
        };

        // Verify and fetch README content
        let readme_str: String;
        match verify_data(body_str.clone()).await {
            false => {
                // If main branch doesn't have a README, try master branch
                let readme: String =
                    get_data(octocrab.clone(), repo.name.clone(), "master".to_string()).await;
                if verify_data(readme.clone()).await == true {
                    readme_str = readme;
                } else {
                    readme_str = "No readme found".to_string();
                }
            }
            true => {
                readme_str = body_str;
            }
        }

        // Store repository data
        data.insert(
            repo.name.clone(),
            Repo {
                name: repo.name.clone(),
                description: repo.description,
                readme: Some(readme_str),
                homepage: repo.homepage,
                url: repo_url,
                stars: repo_stars,
            },
        );
    }

    // Save collected repository data
    save_repos(data).expect("Could not save the repository details");
    Ok(())
}
