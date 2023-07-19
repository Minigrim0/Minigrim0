use octocrab::{Octocrab, params::repos::Commitish};
use hyper::body::to_bytes;

#[tokio::main]
async fn main() -> octocrab::Result<()> {
    let token = std::env::var("GITHUB_TOKEN").expect("GITHUB_TOKEN env variable is required");

    let octocrab = Octocrab::builder().personal_token(token).build()?;

    let my_repos = octocrab
        .current()
        .list_repos_for_authenticated_user()
        .type_("owner")
        .sort("updated")
        .per_page(100)
        .send()
        .await?;

    for repo in my_repos {
        if repo.private.is_some() && repo.private.unwrap() {
            println!("{} is private, skipping", repo.name);
            continue;
        }

        let content: hyper::Response<hyper::Body> = octocrab
            .repos("minigrim0", repo.name.clone())
            .raw_file(Commitish("main".to_string()), "README.md")
            .await
            .expect("Failed to get response !");

        let body = content.into_body();
        let truc = match to_bytes(body).await {
            Ok(val) => val,
            Err(_) => panic!("Could fetch bytes")
        };

        // Convert the response body bytes to a string
        let body_str = String::from_utf8(truc.to_vec()).unwrap();
        println!("================================");
        println!("{}", repo.name);
        println!("================================");
        println!("{}", body_str);
        println!("\n");
    }

    Ok(())
}
