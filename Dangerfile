modified_files = git.modified_files + git.added_files
deleted_files = git.deleted_files

total_lines_changed = git.lines_of_code

summary = "### 🤖 PR 自动摘要\n"
summary += "🚀 **受影响的文件总数**: #{modified_files.count + deleted_files.count}\n"
summary += "🆕 **新增文件**: #{git.added_files.count}\n"
summary += "✏️ **修改的文件**: #{git.modified_files.count}\n"
summary += "🗑️ **删除的文件**: #{git.deleted_files.count}\n"
summary += "📊 **变更的总行数**: #{total_lines_changed}\n"
summary += "📂 **主要修改的文件**:\n"

modified_files.first(5).each do |file|
  summary += "  - `#{file}`\n"
end

unless deleted_files.empty?
  summary += "🗂️ **主要删除的文件**:\n"
  deleted_files.first(5).each do |file|
    summary += "  - `#{file}`\n"
  end
end

warn("PR 描述为空，请提供详细的变更说明。") if github.pr_body.nil? || github.pr_body.strip.empty?

source_branch = github.branch_for_head
target_branch = github.branch_for_base

# warn("PR 目标分支为 `#{target_branch}`，请确保此 PR 遵循合并策略！") if (target_branch == "main" || target_branch == "master") && !(source_branch == "dev" || source_branch == "develop")

warn("PR 被标记为进行中 (WIP)。") if github.pr_title.include? "WIP"

warn("请为此 PR 添加标签。") if github.pr_labels.empty?

markdown(summary)

python_files = (git.modified_files + git.added_files).select { |file| file.end_with?(".py") }

unless python_files.empty?
  flake8_result = `flake8 --ignore=E501 #{python_files.join(" ")}`
  flake8_exit_status = $?.exitstatus
  if flake8_exit_status != 0
    fail("❌ Flake8 检查：\n```\n#{flake8_result}\n```")
  else
    message("✅ Flake8 检查未发现问题！")
  end

  pylint_result = `pylint --disable=C0301,C0114,C0115,C0116 --output-format=parseable #{python_files.join(" ")}`
  pylint_exit_status = $?.exitstatus

  if pylint_exit_status != 0
    fail("❌ Pylint 检查：\n```\n#{pylint_result}\n```")
  else
    message("✅ Pylint 检查未发现问题！")
  end
end
