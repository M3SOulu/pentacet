library(DBI)
library(NLoN)

cmnt_cntr <- 0
db <- 'pentacet'
host_db <- '127.0.0.1'
db_port <- '5432'
db_user <- 'postgres'
db_password <- 'postgres'

con <- dbConnect(RPostgres::Postgres(), dbname = db, host=host_db, port=db_port, user=db_user, password=db_password)
#con <- dbConnect(RPostgreSQL::PostgreSQL(), dbname = db, host=host_db, port=db_port, user=db_user, password=db_password)

update <- function(i) {

cat("updating comment: ", cmnt_cntr)
cat("\n")
cat("model loaded and about to predict for: ", results$comment_content[i])
cat("\n")
nlon_stat <- NLoNPredict(model, results$comment_content[i])[[1]]
cat("nlon_stat: ", nlon_stat)
cat("\n")
cmnt_id <- results$comment_id[i]
cat("about to update comment_id: ", cmnt_id)
cat("\n")
update_query = paste0("UPDATE comment_attr SET nlon_status='",nlon_stat,"' where comment_id='",cmnt_id,"'")
dbExecute(con, update_query)
}

update_cleaned_comment <- function(i) {


cat("updating cleaned comment: ", cmnt_cntr)
cat("\n")
cmnt_id <- results$comment_id[i]
cat("about to update comment_id: ", cmnt_id)
cat("\n")
cln_comment <- results$cleaned_comment[i]
cmnt_id <- gsub("'","''",cmnt_id)
cln_comment <- gsub("'","''",cln_comment)
update_query = paste0("UPDATE comment_attr SET cleaned_comment='",cln_comment,"' where comment_id='",cmnt_id,"'")
dbExecute(con, update_query)
}

update_nlon_stat <- function(cmnt_id,nlon_stat) {
cmnt_id <- gsub("'","''",cmnt_id)
cat("updating for comment_id: ", cmnt_id,"with status ",nlon_stat)
cat("\n")
update_query = paste0("UPDATE comment_attr SET nlon_status='",nlon_stat,"' where comment_id='",cmnt_id,"'")
dbExecute(con, update_query)
}

removeHtml <- function(htmlString) {
    return(gsub("<.*?>", "", htmlString))
}

update_nlon_stat_without_cmnt_sym <- function(cmnt_id,nlon_stat) {
cmnt_id <- gsub("'","''",cmnt_id)
cat("updating for comment_id: ", cmnt_id,"with status ",nlon_stat)
cat("\n")
update_query = paste0("UPDATE comment_attr SET nlon_stat_without_cmnt_sym='",nlon_stat,"' where comment_id='",cmnt_id,"'")
dbExecute(con, update_query)
}


update_cleaned_comment <- function(i) {
cat("updating cleaned comment: ", cmnt_cntr)
cat("\n")
cmnt_id <- results$comment_id[i]
cat("about to update comment_id: ", cmnt_id)
cat("\n")
cln_comment <- results$cleaned_comment[i]
cmnt_id <- gsub("'","''",cmnt_id)
cln_comment <- gsub("'","''",cln_comment)
update_query = paste0("UPDATE comment_attr SET cleaned_comment='",cln_comment,"' where comment_id='",cmnt_id,"'")
dbExecute(con, update_query)
}

results<-dbGetQuery(con, paste("SELECT comment_id, comment_content from comment_attr where cluster_number = '1'"))

comment.re <- "^[:blank:]*(//|\\*|/\\*\\*?|\\*?\\*/)"
cleaned_cmnt <- c(sapply(strsplit(results$comment_content, "\n"), function(lines) {
    paste(sub(comment.re, "", lines), collapse="\n")
}))
cleaned_cmnt <- trimws(cleaned_cmnt)
cleaned_cmnt <- gsub("/[[:space:]|/]*","//",cleaned_cmnt)
cleaned_cmnt <- gsub("-[[:space:]|-]*","---",cleaned_cmnt)
cleaned_cmnt <- gsub("#[[:space:]|#]*","###",cleaned_cmnt)
cleaned_cmnt <- gsub("\\*[[:space:]|\\*]*","***",cleaned_cmnt)
comment.re2 <- "//|---"
cleaned_cmnt <- c(sapply(strsplit(cleaned_cmnt, "\n"), function(lines) {
    paste(gsub(comment.re2, "", lines), collapse="\n")
}))
comment.re3 <- "###"
cleaned_cmnt <- c(sapply(strsplit(cleaned_cmnt, "\n"), function(lines) {
    paste(gsub(comment.re3, "", lines), collapse="\n")
}))
comment.re4 <- '\\*\\*\\*'
cleaned_cmnt <- c(sapply(strsplit(cleaned_cmnt, "\n"), function(lines) {
    paste(gsub(comment.re4, "", lines), collapse="\n")
}))
cleaned_cmnt <- c(sapply(strsplit(cleaned_cmnt, "\n"), function(lines) {
    paste(gsub("<.*?>", "", lines), collapse="\n")
}))
cleaned_cmnt <- trimws(cleaned_cmnt)

results$cleaned_comment <-  cleaned_cmnt
cmnt_cntr <- 0
for (i in 1:nrow(results)) {
  cmnt_cntr <- cmnt_cntr + 1
  update_cleaned_comment(i)
}
