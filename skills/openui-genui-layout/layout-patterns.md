# Layout Patterns

Canonical OpenUI Lang templates for the most common screen patterns.
Select the closest pattern and adapt it — don't invent structure from scratch.

---

## 1. dashboard

**When to use:** Overview with KPIs, charts, and recent activity.

```openui
root = Stack([header, kpi_row, charts_row, recent_section])
header = PageHeader("Dashboard", "System overview")

kpi_row = Grid([kpi1, kpi2, kpi3, kpi4])
kpi1 = StatCard("Total Revenue", "$0", "flat")
kpi2 = StatCard("Active Users", "0", "flat")
kpi3 = StatCard("Conversion", "0%", "flat")
kpi4 = StatCard("Pending", "0", "flat")

charts_row = Grid([revenue_chart, dist_chart])
revenue_chart = Card("Monthly Revenue", [line_chart])
line_chart = LineChart(["Jan","Feb","Mar","Apr","May","Jun"], [series1])
series1 = Series("Revenue", [0,0,0,0,0,0])
dist_chart = Card("Distribution", [pie])
pie = PieChart([])

recent_section = Card("Recent Activity", [recent_table])
recent_table = DataTable(["Date","Description","Amount","Status"], [])
```

---

## 2. crud-list

**When to use:** List with search, filter, pagination, and per-row actions.

```openui
root = Stack([header, toolbar, data_table, pager])
header = PageHeader("Users", "Manage system users")

toolbar = Toolbar([search, role_filter, add_btn])
search = Input("Search users...", "search")
role_filter = Select("All roles", ["Admin","Editor","Viewer"])
add_btn = Button("Add User", "default")

data_table = DataTable(["Name","Email","Role","Status","Actions"], [])
pager = Pagination(1, 10, 0)
```

---

## 3. form-wizard

**When to use:** Registration or multi-step process with per-step validation.

```openui
root = Stack([header, steps_indicator, step_content])
header = PageHeader("New Registration", "Fill in the data in 3 steps")

steps_indicator = Breadcrumb([
  {label: "Basic Data", href: null},
  {label: "Address", href: null},
  {label: "Confirmation", href: null}
])

step_content = Form("step-1", step_buttons, [name_field, email_field, phone_field])
name_field = FormControl("Full name", name_input, null, true)
name_input = Input("John Smith", "text")
email_field = FormControl("Email", email_input, null, true)
email_input = Input("john@example.com", "email")
phone_field = FormControl("Phone", phone_input)
phone_input = Input("(555) 000-0000", "tel")

step_buttons = Buttons([back_btn, next_btn])
back_btn = Button("Back", "outline")
next_btn = Button("Next", "default")
```

---

## 4. detail-view

**When to use:** Viewing details of an entity with sections and tabs.

```openui
root = Stack([breadcrumb, header, info_grid, tabs_section])

breadcrumb = Breadcrumb([
  {label: "Users", href: "/users"},
  {label: "John Smith", href: null}
])

header = PageHeader("John Smith", "Viewing profile")

info_grid = Grid([basic_card, contact_card])
basic_card = Card("Basic Information", [info_list])
info_list = UnorderedList([
  {label: "Role", description: "Administrator"},
  {label: "Status", description: "Active"},
  {label: "Created on", description: "01/01/2024"}
])
contact_card = Card("Contact", [contact_list])
contact_list = UnorderedList([
  {label: "Email", description: "john@example.com"},
  {label: "Phone", description: "(555) 000-0000"}
])

tabs_section = Tabs([activity_tab, permissions_tab])
activity_tab = TabItem("Activity", [activity_table])
activity_table = DataTable(["Date","Action","Details"], [])
permissions_tab = TabItem("Permissions", [permissions_list])
permissions_list = UnorderedList([])
```

---

## 5. settings-page

**When to use:** Settings grouped by category in tabs.

```openui
root = Stack([header, settings_tabs])
header = PageHeader("Settings", "Manage system preferences")

settings_tabs = Tabs([general_tab, notifications_tab, security_tab])

general_tab = TabItem("General", [general_form])
general_form = Form("general-settings", save_buttons, [org_field, tz_field, lang_field])
org_field = FormControl("Organization name", org_input, null, true)
org_input = Input("My Company")
tz_field = FormControl("Time zone", tz_select)
tz_select = Select("America/Sao_Paulo", ["America/Sao_Paulo","America/Fortaleza","America/Manaus"])
lang_field = FormControl("Language", lang_select)
lang_select = Select("Português (BR)", ["Português (BR)","English"])
save_buttons = Buttons([save_btn])
save_btn = Button("Save Changes", "default")

notifications_tab = TabItem("Notifications", [notif_form])
notif_form = Form("notif-settings", notif_buttons, [email_notif, sms_notif])
email_notif = FormControl("Email notifications", email_check)
email_check = Checkbox("Receive alerts by email", true)
sms_notif = FormControl("SMS notifications", sms_check)
sms_check = Checkbox("Receive alerts by SMS", false)
notif_buttons = Buttons([notif_save_btn])
notif_save_btn = Button("Save", "default")

security_tab = TabItem("Security", [pwd_card])
pwd_card = Card("Change Password", [pwd_form])
pwd_form = Form("password", pwd_buttons, [current_pwd, new_pwd, confirm_pwd])
current_pwd = FormControl("Current password", current_input, null, true)
current_input = Input("••••••••", "password")
new_pwd = FormControl("New password", new_input, "Minimum 8 characters", true)
new_input = Input("••••••••", "password")
confirm_pwd = FormControl("Confirm new password", confirm_input, null, true)
confirm_input = Input("••••••••", "password")
pwd_buttons = Buttons([update_pwd_btn])
update_pwd_btn = Button("Update Password", "default")
```

---

## 6. auth-page

**When to use:** Login, registration, password reset.

```openui
root = Stack([auth_card])
auth_card = Card("Sign in to the platform", [auth_form])

auth_form = Form("login", login_buttons, [email_field, password_field])
email_field = FormControl("Email", email_input, null, true)
email_input = Input("you@email.com", "email")
password_field = FormControl("Password", pwd_input, null, true)
pwd_input = Input("••••••••", "password")

login_buttons = Buttons([login_btn, forgot_btn])
login_btn = Button("Sign in", "default")
forgot_btn = Button("Forgot my password", "ghost")
```

---

## 7. empty-state

**When to use:** Initial state with no data, empty search, or unconfigured feature.

```openui
root = Stack([header, empty_card])
header = PageHeader("Documents", "Manage your files")

empty_card = Card(null, [empty_title, empty_desc, empty_actions])
empty_title = TextContent("No documents yet", "h3")
empty_desc = TextContent("Upload your first document to get started.", "muted")
empty_actions = Buttons([upload_btn])
upload_btn = Button("Upload", "default")
```

---

## 8. onboarding

**When to use:** First-steps guide after registration or initial setup.

```openui
root = Stack([welcome_header, progress_alert, steps_grid])

welcome_header = PageHeader("Welcome! Let's get started.", "Complete these steps to set up your account")
progress_alert = Alert("default", "2 of 4 steps completed", "You're doing great!")

steps_grid = Grid([step1, step2, step3, step4])
step1 = Card("Profile configured", [step1_desc, step1_badge])
step1_desc = TextContent("Add your photo and basic information", "small")
step1_badge = Badge("Completed", "default")
step2 = Card("Invite your team", [step2_desc, step2_btn])
step2_desc = TextContent("Add members to collaborate", "small")
step2_btn = Button("Invite", "outline")
step3 = Card("Connect integrations", [step3_desc, step3_btn])
step3_desc = TextContent("Connect your favorite tools", "small")
step3_btn = Button("Explore", "outline")
step4 = Card("Configure notifications", [step4_desc, step4_btn])
step4_desc = TextContent("Choose how to receive alerts", "small")
step4_btn = Button("Configure", "outline")
```

---

## Common Variations

### Dashboard with Sidebar
```openui
root = SidebarLayout(nav_sidebar, [header, kpi_row, charts_row])
nav_sidebar = Sidebar([
  {label: "Dashboard", href: "/"},
  {label: "Users", href: "/users"},
  {label: "Reports", href: "/reports"},
  {label: "Settings", href: "/settings"}
])
# ... continues with the dashboard pattern
```

### CRUD with Sheet (no modal)
```openui
root = Stack([header, toolbar, data_table, pager, edit_sheet])
edit_sheet = Sheet("right", "Edit Record", [edit_form])
edit_form = Form("edit-record", edit_buttons, [name_field, email_field])
# ...
```

### Detail View with actions in the header
```openui
root = Stack([breadcrumb, header_with_actions, info_section])
header_with_actions = PageHeader("John Smith", null, [edit_btn, delete_btn])
edit_btn = Button("Edit", "outline")
delete_btn = Button("Delete", "destructive")
# ...
```

---

## Quick Selection Table

| Situation | Pattern |
|----------|--------|
| Landing screen with numbers | `dashboard` |
| List/search/filter entities | `crud-list` |
| Create entity with many fields | `form-wizard` |
| View details of an entity | `detail-view` |
| Configure system/user | `settings-page` |
| Login/registration/reset | `auth-page` |
| Empty feature or no data | `empty-state` |
| First steps after registration | `onboarding` |
