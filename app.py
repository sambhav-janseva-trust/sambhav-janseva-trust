from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ==============================
# UPLOAD FOLDERS
# ==============================

UPLOAD_FOLDER = "uploads/members"
VOLUNTEER_UPLOAD_FOLDER = "uploads/volunteers"
PHOTOGRAPH_UPLOAD_FOLDER = "uploads/photographs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["VOLUNTEER_UPLOAD_FOLDER"] = VOLUNTEER_UPLOAD_FOLDER
app.config["PHOTOGRAPH_UPLOAD_FOLDER"] = PHOTOGRAPH_UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VOLUNTEER_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PHOTOGRAPH_UPLOAD_FOLDER, exist_ok=True)

# ==============================
# SECRET KEY
# ==============================

app.secret_key = os.environ["SECRET_KEY"]

# ==============================
# DATABASE
# ==============================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "sambhav_janseva.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================================
# MEMBER MODEL
# ============================================================

class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # IMPORTANT: Existing database required this field
    member_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))

    address = db.Column(db.Text)
    village = db.Column(db.String(100))
    post = db.Column(db.String(100))
    police_station = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))

    id_proof_type = db.Column(db.String(50))
    id_proof_number = db.Column(db.String(100))

    occupation = db.Column(db.String(100))
    education = db.Column(db.String(100))

    membership_date = db.Column(db.String(20))
    membership_type = db.Column(db.String(50))
    status = db.Column(db.String(30), default="Active")

    photo = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    id_proof = db.Column(db.String(255))
    address_proof = db.Column(db.String(255))


# ============================================================
# VOLUNTEER MODEL
# ============================================================

class Volunteer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # IMPORTANT: Existing database required this field
    volunteer_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))

    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))

    address = db.Column(db.Text)
    village = db.Column(db.String(100))
    post = db.Column(db.String(100))
    police_station = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))

    education = db.Column(db.String(100))
    occupation = db.Column(db.String(100))

    joining_date = db.Column(db.String(20))
    status = db.Column(db.String(30), default="Active")

    photo = db.Column(db.String(255))
    signature = db.Column(db.String(255))

    area = db.Column(db.String(100))
    volunteer_type = db.Column(db.String(100), default="General")
    skills = db.Column(db.Text)


# ============================================================
# ASSISTANCE APPLICATION MODEL
# ============================================================

class AssistanceApplication(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # IMPORTANT: Existing database required this field
    application_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # Keep application_no also for existing templates/data
    application_no = db.Column(
        db.String(50),
        unique=True
    )

    applicant_name = db.Column(
        db.String(100),
        nullable=False
    )

    father_name = db.Column(db.String(100))

    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))

    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))

    address = db.Column(db.Text)

    village = db.Column(db.String(100))
    post = db.Column(db.String(100))
    police_station = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))

    assistance_type = db.Column(db.String(100))
    assistance_amount = db.Column(db.String(50))

    reason = db.Column(db.Text)

    application_date = db.Column(db.String(20))

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    remarks = db.Column(db.Text)


# ============================================================
# DONATION MODEL
# ============================================================

class Donation(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    donation_date = db.Column(
        db.String(20)
    )

    donation_type = db.Column(
        db.String(30),
        default="One Time"
    )

    donor_name = db.Column(
        db.String(150),
        nullable=False
    )

    mobile = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(150)
    )

    address = db.Column(
        db.Text
    )

    pan = db.Column(
        db.String(30)
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0
    )

    purpose = db.Column(
        db.String(200)
    )

    payment_mode = db.Column(
        db.String(50)
    )

    transaction_reference = db.Column(
        db.String(150)
    )

    payment_status = db.Column(
        db.String(30),
        default="Received"
    )

    remarks = db.Column(
        db.Text
    )


# ============================================================
# PROGRAM / EVENT MODEL
# ============================================================

class Program(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    program_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    program_type = db.Column(
        db.String(50),
        default="Program"
    )

    program_date = db.Column(
        db.String(20)
    )

    start_time = db.Column(
        db.String(20)
    )

    end_time = db.Column(
        db.String(20)
    )

    venue = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Upcoming"
    )

    remarks = db.Column(
        db.Text
    )
class Photograph(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    program = db.Column(db.String(200), nullable=False)

    photo_date = db.Column(db.String(20))

    description = db.Column(db.Text)

    filename = db.Column(db.String(255), nullable=False)

    uploaded_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

@app.route("/admin/photographs/add", methods=["GET", "POST"])
def add_photograph():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        program = request.form.get("program", "").strip()
        photo_date = request.form.get("photo_date", "").strip()
        description = request.form.get("description", "").strip()

        photograph = request.files.get("photograph")

        if not title:
            return """<script>
                alert("Photograph Title is required.");
                window.history.back();
            </script>"""

        if not program:
            return """<script>
                alert("Program / Event name is required.");
                window.history.back();
            </script>"""

        if not photograph or not photograph.filename:
            return """<script>
                alert("Please select a photograph.");
                window.history.back();
            </script>"""

        filename = photograph.filename

        photograph.save(
            os.path.join(
                app.config["PHOTOGRAPH_UPLOAD_FOLDER"],
                filename
            )
        )

        new_photograph = Photograph(
            title=title,
            program=program,
            photo_date=photo_date,
            description=description,
            filename=filename
        )

        db.session.add(new_photograph)
        db.session.commit()

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "add_photographs.html"
    )
@app.route("/admin/photographs")
def admin_photographs():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    photographs = Photograph.query.order_by(
        Photograph.id.desc()
    ).all()

    return render_template(
        "photographs.html",
        photographs=photographs
    )


@app.route("/uploads/photographs/<filename>")
def photograph_file(filename):

    return send_from_directory(
        app.config["PHOTOGRAPH_UPLOAD_FOLDER"],
        filename
    )
@app.route("/admin/photographs/<int:photograph_id>/download")
def download_photograph(photograph_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    photograph = Photograph.query.get_or_404(photograph_id)

    return send_from_directory(
        app.config["PHOTOGRAPH_UPLOAD_FOLDER"],
        photograph.filename,
        as_attachment=True
    )


@app.route("/admin/photographs/<int:photograph_id>/delete", methods=["POST"])
def delete_photograph(photograph_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    photograph = Photograph.query.get_or_404(photograph_id)

    file_path = os.path.join(
        app.config["PHOTOGRAPH_UPLOAD_FOLDER"],
        photograph.filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(photograph)
    db.session.commit()

    return redirect(url_for("admin_photographs"))
@app.route("/admin/photographs/<int:photograph_id>")
def view_photograph(photograph_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    photograph = Photograph.query.get_or_404(photograph_id)

    return render_template(
        "photograph_view.html",
        photograph=photograph
    )


@app.route("/admin/photographs/<int:photograph_id>/edit", methods=["GET", "POST"])
def edit_photograph(photograph_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    photograph = Photograph.query.get_or_404(photograph_id)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        program = request.form.get("program", "").strip()
        photo_date = request.form.get("photo_date", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            return """<script>alert("Photograph Title is required.");window.history.back();</script>"""

        if not program:
            return """<script>alert("Program / Event name is required.");window.history.back();</script>"""

        photograph.title = title
        photograph.program = program
        photograph.photo_date = photo_date
        photograph.description = description

        db.session.commit()

        return redirect(
            url_for("view_photograph", photograph_id=photograph.id)
        )

    return render_template(
        "edit_photograph.html",
        photograph=photograph
    )
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notice_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="Published")
    created_at = db.Column(db.DateTime, default=db.func.now())


class WebsiteHomeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(300))
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
# ============================================================
# ADD PROGRAM / EVENT
# ============================================================

@app.route(
    "/admin/programs/add",
    methods=["GET", "POST"]
)
def add_program():

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        program_type = request.form.get(
            "program_type",
            "Program"
        ).strip()

        program_date = request.form.get(
            "program_date",
            ""
        ).strip()

        start_time = request.form.get(
            "start_time",
            ""
        ).strip()

        end_time = request.form.get(
            "end_time",
            ""
        ).strip()

        venue = request.form.get(
            "venue",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Upcoming"
        ).strip()

        remarks = request.form.get(
            "remarks",
            ""
        ).strip()

        if not title:
            return """
            <script>
                alert("Program / Event Title is required.");
                window.history.back();
            </script>
            """

        existing_programs = Program.query.all()

        highest_number = 0

        for existing_program in existing_programs:

            existing_id = (
                existing_program.program_id or ""
            ).strip()

            if existing_id.startswith("PRG-"):

                try:
                    number = int(
                        existing_id.replace(
                            "PRG-",
                            ""
                        )
                    )

                    if number > highest_number:
                        highest_number = number

                except ValueError:
                    pass

        program_id = "PRG-{0:03d}".format(
            highest_number + 1
        )

        program = Program(
            program_id=program_id,
            title=title,
            program_type=program_type,
            program_date=program_date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            description=description,
            status=status,
            remarks=remarks
        )

        db.session.add(program)
        db.session.commit()

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "add_program.html"
    )

@app.route("/admin/notices/add", methods=["GET", "POST"])
def add_notice():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        notice_date = request.form.get("notice_date", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Published").strip()

        if not title:
            return """<script>
                alert("Notice Title is required.");
                window.history.back();
            </script>"""

        if not description:
            return """<script>
                alert("Notice Description is required.");
                window.history.back();
            </script>"""

        notice = Notice(
            title=title,
            notice_date=notice_date,
            description=description,
            status=status
        )

        db.session.add(notice)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_notice.html")
@app.route("/admin/notices")
def admin_notices():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    notices = Notice.query.order_by(
        Notice.id.desc()
    ).all()

    return render_template(
        "notices.html",
        notices=notices
    )
@app.route("/admin/notices/<int:notice_id>")
def view_notice(notice_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    notice = Notice.query.get_or_404(notice_id)

    return render_template(
        "view_notice.html",
        notice=notice
    )
@app.route("/admin/notices/<int:notice_id>/edit", methods=["GET", "POST"])
def edit_notice(notice_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    notice = Notice.query.get_or_404(notice_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        notice_date = request.form.get("notice_date", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Published").strip()

        if not title:
            return """<script>
                alert("Notice Title is required.");
                window.history.back();
            </script>"""

        if not description:
            return """<script>
                alert("Notice Description is required.");
                window.history.back();
            </script>"""

        notice.title = title
        notice.notice_date = notice_date
        notice.description = description
        notice.status = status

        db.session.commit()

        return redirect(url_for(
            "view_notice",
            notice_id=notice.id
        ))

    return render_template(
        "edit_notice.html",
        notice=notice
    )

@app.route("/admin/notices/<int:notice_id>/delete", methods=["GET", "POST"])
def delete_notice(notice_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    notice = Notice.query.get_or_404(notice_id)

    db.session.delete(notice)
    db.session.commit()

    return redirect(url_for("admin_notices"))
@app.route("/notices")
def public_notices():
    notices = Notice.query.filter_by(
        status="Published"
    ).order_by(
        Notice.id.desc()
    ).all()

    return render_template(
        "public_notices.html",
        notices=notices
    )
@app.route("/notices/<int:notice_id>")
def public_notice_detail(notice_id):
    notice = Notice.query.filter_by(
        id=notice_id,
        status="Published"
    ).first_or_404()

    return render_template(
        "public_notice_detail.html",
        notice=notice
    )
# ============================================================
# PROGRAM / EVENT LIST
# ============================================================

@app.route("/admin/programs")
def admin_programs():

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("admin_login")
        )

    programs = (
        Program.query
        .order_by(Program.id.desc())
        .all()
    )

    return render_template(
        "programs.html",
        programs=programs
    )

# ============================================================
# PROGRAM / EVENT VIEW
# ============================================================

@app.route("/admin/programs/<int:program_id>")
def view_program(program_id):

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("admin_login")
        )

    program = Program.query.get_or_404(program_id)

    return render_template(
        "program_view.html",
        program=program
    )

# ============================================================
# PROGRAM / EVENT DELETE
# ============================================================

@app.route("/admin/programs/<int:program_id>/delete", methods=["POST"])
def delete_program(program_id):

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("admin_login")
        )

    program = Program.query.get_or_404(program_id)

    db.session.delete(program)
    db.session.commit()

    return redirect(
        url_for("admin_programs")
    )
# ============================================================
# PROGRAM / EVENT EDIT
# ============================================================

@app.route("/admin/programs/<int:program_id>/edit", methods=["GET", "POST"])
def edit_program(program_id):

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("admin_login")
        )

    program = Program.query.get_or_404(program_id)

    if request.method == "POST":

        program.title = request.form.get("title", "").strip()
        program.program_type = request.form.get("program_type", "Program").strip()
        program.program_date = request.form.get("program_date", "").strip()
        program.start_time = request.form.get("start_time", "").strip()
        program.end_time = request.form.get("end_time", "").strip()
        program.venue = request.form.get("venue", "").strip()
        program.description = request.form.get("description", "").strip()
        program.status = request.form.get("status", "Upcoming").strip()
        program.remarks = request.form.get("remarks", "").strip()

        if not program.title:
            return """<script>
            alert("Program / Event Title is required.");
            window.history.back();
            </script>"""

        db.session.commit()

        return redirect(
            url_for("view_program", program_id=program.id)
        )

    return render_template(
        "edit_program.html",
        program=program
    )
# ============================================================
# PUBLIC HOME PAGE
# ============================================================

@app.route("/")
def home():

    home_content = WebsiteHomeContent.query.first()
    about_content = WebsiteAboutContent.query.first()
    contact_content = WebsiteContactContent.query.first()
    future_content = WebsiteFutureContent.query.first()

    if not home_content:
        home_content = WebsiteHomeContent(
            title="Sambhav Janseva Trust",
            subtitle="सेवा और सहयोग",
            description="जनसेवा और समाज के जरूरतमंद लोगों की सहायता के लिए समर्पित।"
        )

    if not about_content:
        about_content = WebsiteAboutContent(
            heading="Sambhav Janseva Trust के बारे में",
            description=""
        )

    if not contact_content:
        contact_content = WebsiteContactContent(
            email="",
            mobile="",
            address=""
        )

    if not future_content:
        future_content = WebsiteFutureContent(
            heading="",
            description=""
        )

    return render_template(
        "public_home.html",
        content=home_content,
        about_content=about_content,
        contact_content=contact_content,
        future_content=future_content
    )

# ============================================================
# WEBSITE ABOUT TRUST CONTENT
# ============================================================

class WebsiteAboutContent(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    heading = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )


# ============================================================
# PUBLIC WEBSITE HOME
# ============================================================

@app.route("/website")
def public_home():

    home_content = WebsiteHomeContent.query.first()
    about_content = WebsiteAboutContent.query.first()
    contact_content = WebsiteContactContent.query.first()
    future_content = WebsiteFutureContent.query.first()

    if not home_content:
        home_content = WebsiteHomeContent(
            title="Sambhav Janseva Trust",
            subtitle="सेवा और सहयोग",
            description="जनसेवा और समाज के जरूरतमंद लोगों की सहायता के लिए समर्पित।"
        )

    if not about_content:
        about_content = WebsiteAboutContent(
            heading="Sambhav Janseva Trust के बारे में",
            description=""
        )

    if not contact_content:
        contact_content = WebsiteContactContent(
            email="",
            mobile="",
            address=""
        )

    if not future_content:
        future_content = WebsiteFutureContent(
            heading="",
            description=""
        )

    return render_template(
        "public_home.html",
        content=home_content,
        about_content=about_content,
        contact_content=contact_content,
        future_content=future_content
    )

# ============================================================
# WEBSITE CONTACT CONTENT
# ============================================================

class WebsiteContactContent(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(200)
    )

    mobile = db.Column(
        db.String(30)
    )

    address = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )
# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if (
        username == os.environ["ADMIN_USERNAME"]
        and password == os.environ["ADMIN_PASSWORD"]
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return """
        <script>
            alert("Invalid username or password");
            window.history.back();
        </script>
        """

    return render_template(
        "admin_login.html"
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    total_members = Member.query.count()

    total_volunteers = Volunteer.query.count()

    total_assistance = (
        AssistanceApplication.query.count()
    )

    total_donations = Donation.query.count()

    total_donation_amount = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(Donation.amount),
                0
            )
        ).scalar()
        or 0
    )

    return render_template(
        "admin_dashboard.html",

        total_members=total_members,

        total_volunteers=total_volunteers,

        total_assistance=total_assistance,

        total_donations=total_donations,

        total_donation_amount=total_donation_amount
    )


# ============================================================
# FOUNDER PROFILE
# ============================================================

@app.route("/founder-profile")
def founder_profile():

    return render_template(
        "founder_profile.html"
    )

@app.route("/admin/website-content")
def website_content():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("website_content.html")

@app.route("/admin/website-content/home", methods=["GET", "POST"])
def edit_home_content():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    content = WebsiteHomeContent.query.first()

    if not content:
        content = WebsiteHomeContent(
            title="",
            subtitle="",
            description=""
        )
        db.session.add(content)
        db.session.commit()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subtitle = request.form.get("subtitle", "").strip()
        description = request.form.get("description", "").strip()

        content.title = title
        content.subtitle = subtitle
        content.description = description

        db.session.commit()

        return redirect(url_for("website_content"))

    return render_template(
        "edit_home_content.html",
        content=content
    )

# ============================================================
# EDIT ABOUT TRUST CONTENT
# ============================================================

@app.route("/admin/website-content/about", methods=["GET", "POST"])
def edit_about_content():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    content = WebsiteAboutContent.query.first()

    if not content:

        content = WebsiteAboutContent(
            heading="",
            description=""
        )

        db.session.add(content)
        db.session.commit()

    if request.method == "POST":

        heading = request.form.get(
            "heading",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        content.heading = heading
        content.description = description

        db.session.commit()

        return redirect(
            url_for("website_content")
        )

    return render_template(
        "edit_about_content.html",
        content=content
    )

# ============================================================
# EDIT CONTACT INFORMATION
# ============================================================

@app.route("/admin/website-content/contact", methods=["GET", "POST"])
def edit_contact_content():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    content = WebsiteContactContent.query.first()

    if not content:

        content = WebsiteContactContent(
            email="",
            mobile="",
            address=""
        )

        db.session.add(content)
        db.session.commit()

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        content.email = email
        content.mobile = mobile
        content.address = address

        db.session.commit()

        return redirect(
            url_for("website_content")
        )

    return render_template(
        "edit_contact_content.html",
        content=content
    )

    # ============================================================
# WEBSITE FUTURE CONTENT
# ============================================================

class WebsiteFutureContent(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    heading = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    # ============================================================
# EDIT FUTURE CONTENT
# ============================================================

@app.route("/admin/website-content/future", methods=["GET", "POST"])
def edit_future_content():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    content = WebsiteFutureContent.query.first()

    if not content:

        content = WebsiteFutureContent(
            heading="",
            description=""
        )

        db.session.add(content)
        db.session.commit()

    if request.method == "POST":

        heading = request.form.get(
            "heading",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        content.heading = heading
        content.description = description

        db.session.commit()

        return redirect(
            url_for("website_content")
        )

    return render_template(
        "edit_future_content.html",
        content=content
    )
# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect(
        url_for("admin_login")
    )


# ============================================================
# ASSISTANCE APPLICATION - ADD
# ============================================================

@app.route(
    "/admin/assistance/add",
    methods=["GET", "POST"]
)
def add_assistance():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        applicant_name = request.form.get(
            "applicant_name",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        dob = request.form.get(
            "dob",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        village = request.form.get(
            "village",
            ""
        ).strip()

        post = request.form.get(
            "post",
            ""
        ).strip()

        police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        assistance_type = request.form.get(
            "assistance_type",
            ""
        ).strip()

        assistance_amount = request.form.get(
            "assistance_amount",
            ""
        ).strip()

        reason = request.form.get(
            "reason",
            ""
        ).strip()

        application_date = request.form.get(
            "application_date",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Pending"
        ).strip()

        remarks = request.form.get(
            "remarks",
            ""
        ).strip()

        if not applicant_name:

            return """
            <script>
                alert("Applicant name is required");
                window.history.back();
            </script>
            """

        last_application = (
            AssistanceApplication.query
            .order_by(
                AssistanceApplication.id.desc()
            )
            .first()
        )

        if last_application is None:
            next_number = 1
        else:
            next_number = (
                last_application.id + 1
            )

        application_id = (
            f"SJT-A-{next_number:05d}"
        )

        application_no = application_id

        application = AssistanceApplication(

            application_id=application_id,

            application_no=application_no,

            applicant_name=applicant_name,

            father_name=father_name,

            dob=dob,

            gender=gender,

            mobile=mobile,

            email=email,

            address=address,

            village=village,

            post=post,

            police_station=police_station,

            district=district,

            state=state,

            pincode=pincode,

            assistance_type=assistance_type,

            assistance_amount=assistance_amount,

            reason=reason,

            application_date=application_date,

            status=status,

            remarks=remarks
        )

        db.session.add(application)

        db.session.commit()

        return redirect(
            url_for(
                "view_assistance",
                application_id=application.id
            )
        )

    return render_template(
        "add_assistance.html"
    )


# ============================================================
# ASSISTANCE APPLICATION - DELETE
# ============================================================

@app.route(
    "/admin/assistance/<int:application_id>/delete",
    methods=["POST"]
)
def delete_assistance(application_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    application = (
        AssistanceApplication.query.get_or_404(
            application_id
        )
    )

    db.session.delete(application)

    db.session.commit()

    return redirect(
        url_for("assistance_list")
    )


# ============================================================
# ASSISTANCE APPLICATION - LIST
# ============================================================

@app.route("/admin/assistance")
def assistance_list():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    applications = (
        AssistanceApplication.query
        .order_by(
            AssistanceApplication.id.desc()
        )
        .all()
    )

    return render_template(
        "assistance_list.html",
        applications=applications
    )


# ============================================================
# ASSISTANCE APPLICATION - VIEW
# ============================================================

@app.route(
    "/admin/assistance/<int:application_id>"
)
def view_assistance(application_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    application = (
        AssistanceApplication.query.get_or_404(
            application_id
        )
    )

    return render_template(
        "assistance_view.html",
        application=application
    )


# ============================================================
# ASSISTANCE APPLICATION - UPDATE STATUS
# ============================================================

@app.route(
    "/admin/assistance/<int:application_id>/status",
    methods=["POST"]
)
def update_assistance_status(application_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    application = (
        AssistanceApplication.query.get_or_404(
            application_id
        )
    )

    new_status = request.form.get(
        "status",
        "Pending"
    ).strip()

    new_remarks = request.form.get(
        "remarks",
        ""
    ).strip()

    application.status = new_status
    application.remarks = new_remarks

    db.session.commit()

    return redirect(
        url_for(
            "view_assistance",
            application_id=application.id
        )
    )


# ============================================================
# ASSISTANCE APPLICATION - EDIT
# ============================================================

@app.route(
    "/admin/assistance/<int:application_id>/edit",
    methods=["GET", "POST"]
)
def edit_assistance(application_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    application = (
        AssistanceApplication.query.get_or_404(
            application_id
        )
    )

    if request.method == "POST":

        applicant_name = request.form.get(
            "applicant_name",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        dob = request.form.get(
            "dob",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        village = request.form.get(
            "village",
            ""
        ).strip()

        post = request.form.get(
            "post",
            ""
        ).strip()

        police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        assistance_type = request.form.get(
            "assistance_type",
            ""
        ).strip()

        assistance_amount = request.form.get(
            "assistance_amount",
            ""
        ).strip()

        reason = request.form.get(
            "reason",
            ""
        ).strip()

        application_date = request.form.get(
            "application_date",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Pending"
        ).strip()

        remarks = request.form.get(
            "remarks",
            ""
        ).strip()

        if not applicant_name:

            return """
            <script>
                alert("Applicant name is required");
                window.history.back();
            </script>
            """

        application.applicant_name = applicant_name
        application.father_name = father_name
        application.dob = dob
        application.gender = gender
        application.mobile = mobile
        application.email = email
        application.address = address
        application.village = village
        application.post = post
        application.police_station = police_station
        application.district = district
        application.state = state
        application.pincode = pincode
        application.assistance_type = assistance_type
        application.assistance_amount = assistance_amount
        application.reason = reason
        application.application_date = application_date
        application.status = status
        application.remarks = remarks

        db.session.commit()

        return redirect(
            url_for(
                "view_assistance",
                application_id=application.id
            )
        )

    return render_template(
        "edit_assistance.html",
        application=application
    )
# ============================================================
# MEMBER - UPLOADED FILE
# ============================================================

@app.route(
    "/uploads/members/<path:filename>"
)
def uploaded_member_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ============================================================
# MEMBER - ADD
# ============================================================

@app.route(
    "/admin/members/add",
    methods=["GET", "POST"]
)
def add_member():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        dob = request.form.get(
            "dob",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        village = request.form.get(
            "village",
            ""
        ).strip()

        post = request.form.get(
            "post",
            ""
        ).strip()

        police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        id_proof_type = request.form.get(
            "id_proof_type",
            ""
        ).strip()

        id_proof_number = request.form.get(
            "id_proof_number",
            ""
        ).strip()

        occupation = request.form.get(
            "occupation",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        membership_date = request.form.get(
            "membership_date",
            ""
        ).strip()
        membership_type = request.form.get(
    "membership_type",
    ""
).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()

        if not name:

            return """
            <script>
                alert("Member name is required");
                window.history.back();
            </script>
            """

        # ----------------------------------------------------
        # GENERATE MEMBER ID
        # ----------------------------------------------------

        last_member = (
            Member.query
            .order_by(
                Member.id.desc()
            )
            .first()
        )

        if last_member is None:
            next_number = 1
        else:
            next_number = last_member.id + 1

        member_id = (
            f"SJT-M-{next_number:05d}"
        )

        # ----------------------------------------------------
        # FILES
        # ----------------------------------------------------

        photo = request.files.get(
            "photo"
        )

        signature = request.files.get(
            "signature"
        )

        id_proof = request.files.get(
            "id_proof"
        )

        address_proof = request.files.get(
            "address_proof"
        )

        photo_filename = None
        signature_filename = None
        id_proof_filename = None
        address_proof_filename = None

        if photo and photo.filename:

            photo_filename = photo.filename

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    photo_filename
                )
            )

        if signature and signature.filename:

            signature_filename = signature.filename

            signature.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    signature_filename
                )
            )

        if id_proof and id_proof.filename:

            id_proof_filename = id_proof.filename

            id_proof.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    id_proof_filename
                )
            )

        if (
            address_proof
            and address_proof.filename
        ):

            address_proof_filename = (
                address_proof.filename
            )

            address_proof.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    address_proof_filename
                )
            )

        # ----------------------------------------------------
        # CREATE MEMBER
        # ----------------------------------------------------

        member = Member(

            member_id=member_id,

            name=name,

            father_name=father_name,

            dob=dob,

            gender=gender,

            mobile=mobile,

            email=email,

            address=address,

            village=village,

            post=post,

            police_station=police_station,

            district=district,

            state=state,

            pincode=pincode,

            id_proof_type=id_proof_type,

            id_proof_number=id_proof_number,

            occupation=occupation,

            education=education,

            membership_date=membership_date,

            membership_type=membership_type,

            status=status,

            photo=photo_filename,

            signature=signature_filename,

            id_proof=id_proof_filename,

            address_proof=address_proof_filename
        )

        db.session.add(member)

        db.session.commit()

        return redirect(
            url_for(
                "view_member",
                member_id=member.id
            )
        )

    return render_template(
        "add_member.html"
    )


# ============================================================
# MEMBER - LIST
# ============================================================

@app.route("/admin/members")
def members_list():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    search = request.args.get(
        "search",
        ""
    ).strip()

    if search:

        members = Member.query.filter(
            db.or_(
                Member.name.ilike(
                    f"%{search}%"
                ),
                Member.mobile.ilike(
                    f"%{search}%"
                ),
                Member.email.ilike(
                    f"%{search}%"
                )
            )
        ).order_by(
            Member.id.desc()
        ).all()

    else:

        members = (
            Member.query
            .order_by(
                Member.id.desc()
            )
            .all()
        )

    return render_template(
        "members.html",
        members=members,
        search=search
    )


# ============================================================
# MEMBER - VIEW
# ============================================================

@app.route(
    "/admin/members/<int:member_id>"
)
def view_member(member_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    member = (
        Member.query.get_or_404(
            member_id
        )
    )

    return render_template(
        "member_view.html",
        member=member
    )


# ============================================================
# MEMBER - EDIT
# ============================================================

@app.route(
    "/admin/members/<int:member_id>/edit",
    methods=["GET", "POST"]
)
def edit_member(member_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    member = (
        Member.query.get_or_404(
            member_id
        )
    )

    if request.method == "POST":

        member.name = request.form.get(
            "name",
            ""
        ).strip()

        member.father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        member.dob = request.form.get(
            "dob",
            ""
        ).strip()

        member.gender = request.form.get(
            "gender",
            ""
        ).strip()

        member.mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        member.email = request.form.get(
            "email",
            ""
        ).strip()

        member.address = request.form.get(
            "address",
            ""
        ).strip()

        member.village = request.form.get(
            "village",
            ""
        ).strip()

        member.post = request.form.get(
            "post",
            ""
        ).strip()

        member.police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        member.district = request.form.get(
            "district",
            ""
        ).strip()

        member.state = request.form.get(
            "state",
            ""
        ).strip()

        member.pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        member.id_proof_type = request.form.get(
            "id_proof_type",
            ""
        ).strip()

        member.id_proof_number = request.form.get(
            "id_proof_number",
            ""
        ).strip()

        member.occupation = request.form.get(
            "occupation",
            ""
        ).strip()

        member.education = request.form.get(
            "education",
            ""
        ).strip()

        member.membership_date = request.form.get(
            "membership_date",
            ""
        ).strip()

        member.membership_type = request.form.get(
            "membership_type",
            ""
        ).strip()

        member.status = request.form.get(
            "status",
            "Active"
        ).strip()

        photo = request.files.get(
            "photo"
        )

        signature = request.files.get(
            "signature"
        )

        id_proof = request.files.get(
            "id_proof"
        )

        address_proof = request.files.get(
            "address_proof"
        )

        if photo and photo.filename:

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    photo.filename
                )
            )

            member.photo = photo.filename

        if signature and signature.filename:

            signature.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    signature.filename
                )
            )

            member.signature = signature.filename

        if id_proof and id_proof.filename:

            id_proof.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    id_proof.filename
                )
            )

            member.id_proof = id_proof.filename

        if (
            address_proof
            and address_proof.filename
        ):

            address_proof.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    address_proof.filename
                )
            )

            member.address_proof = (
                address_proof.filename
            )

        db.session.commit()

        return redirect(
            url_for(
                "view_member",
                member_id=member.id
            )
        )

    return render_template(
        "edit_member.html",
        member=member
    )
# ============================================================
# MEMBER - DELETE
# ============================================================

@app.route(
    "/admin/members/<int:member_id>/delete",
    methods=["POST"]
)
def delete_member(member_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    member = (
        Member.query.get_or_404(
            member_id
        )
    )

    db.session.delete(member)

    db.session.commit()

    return redirect(
        url_for("members_list")
    )


# ============================================================
# VOLUNTEER - LIST
# ============================================================

@app.route("/admin/volunteers")
def volunteers_list():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    volunteers = (
        Volunteer.query
        .order_by(
            Volunteer.id.desc()
        )
        .all()
    )

    return render_template(
        "volunteers.html",
        volunteers=volunteers
    )


# ============================================================
# VOLUNTEER - ADD
# ============================================================

@app.route(
    "/admin/volunteers/add",
    methods=["GET", "POST"]
)
def add_volunteer():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        dob = request.form.get(
            "dob",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        village = request.form.get(
            "village",
            ""
        ).strip()

        post = request.form.get(
            "post",
            ""
        ).strip()

        police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        occupation = request.form.get(
            "occupation",
            ""
        ).strip()

        area = request.form.get(
            "area",
            ""
        ).strip()

        volunteer_type = request.form.get(
            "volunteer_type",
            "General"
        ).strip()

        joining_date = request.form.get(
            "joining_date",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()

        if not name:

            return """
            <script>
                alert("Volunteer name is required");
                window.history.back();
            </script>
            """

        # ----------------------------------------------------
        # GENERATE VOLUNTEER ID
        # ----------------------------------------------------

        last_volunteer = (
            Volunteer.query
            .order_by(
                Volunteer.id.desc()
            )
            .first()
        )

        if last_volunteer is None:
            next_number = 1
        else:
            next_number = (
                last_volunteer.id + 1
            )

        volunteer_id = (
            f"SJT-V-{next_number:05d}"
        )

        # ----------------------------------------------------
        # FILES
        # ----------------------------------------------------

        photo = request.files.get(
            "photo"
        )

        signature = request.files.get(
            "signature"
        )

        photo_filename = None
        signature_filename = None

        if photo and photo.filename:

            photo_filename = (
                f"{volunteer_id}_photo_{photo.filename}"
            )

            photo.save(
                os.path.join(
                    app.config["VOLUNTEER_UPLOAD_FOLDER"],
                    photo_filename
                )
            )

        if signature and signature.filename:

            signature_filename = (
                f"{volunteer_id}_signature_{signature.filename}"
            )

            signature.save(
                os.path.join(
                    app.config["VOLUNTEER_UPLOAD_FOLDER"],
                    signature_filename
                )
            )

        # ----------------------------------------------------
        # CREATE VOLUNTEER
        # ----------------------------------------------------

        volunteer = Volunteer(

            volunteer_id=volunteer_id,

            name=name,

            father_name=father_name,

            dob=dob,

            gender=gender,

            mobile=mobile,

            email=email,

            address=address,

            village=village,

            post=post,

            police_station=police_station,

            district=district,

            state=state,

            pincode=pincode,

            education=education,

            occupation=occupation,

            area=area,

            volunteer_type=volunteer_type,

            joining_date=joining_date,

            skills=skills,

            status=status,

            photo=photo_filename,

            signature=signature_filename
        )

        db.session.add(volunteer)

        db.session.commit()

        return redirect(
            url_for(
                "view_volunteer",
                volunteer_id=volunteer.id
            )
        )

    return render_template(
        "add_volunteer.html"
    )



# ============================================================
# VOLUNTEER - VIEW
# ============================================================

@app.route(
    "/admin/volunteers/<int:volunteer_id>"
)
def view_volunteer(volunteer_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    volunteer = (
        Volunteer.query.get_or_404(
            volunteer_id
        )
    )

    return render_template(
        "view_volunteer.html",
        volunteer=volunteer
    )


# ============================================================
# VOLUNTEER - ID CARD
# ============================================================

@app.route(
    "/admin/volunteers/<int:volunteer_id>/id-card"
)
def volunteer_id_card(volunteer_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    volunteer = (
        Volunteer.query.get_or_404(
            volunteer_id
        )
    )

    return render_template(
        "volunteer_id_card.html",
        volunteer=volunteer
    )


# ============================================================
# VOLUNTEER FILE ROUTE
#
# SAME ENDPOINT SUPPORTS:
# 1. GET  -> display uploaded volunteer photo/signature
# 2. POST -> upload/update volunteer photo/signature
#
# This fixes the BuildError where view_volunteer.html
# sends filename=... to endpoint volunteer_upload.
# ============================================================

@app.route(
    "/uploads/volunteers/<path:filename>",
    methods=["GET"],
    endpoint="volunteer_upload"
)
@app.route(
    "/admin/volunteers/<int:volunteer_id>/upload",
    methods=["POST"],
    endpoint="volunteer_upload"
)
def volunteer_upload(
    filename=None,
    volunteer_id=None
):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    # --------------------------------------------------------
    # DISPLAY PHOTO / SIGNATURE
    # --------------------------------------------------------

    if request.method == "GET":

        return send_from_directory(
            app.config["VOLUNTEER_UPLOAD_FOLDER"],
            filename
        )

    # --------------------------------------------------------
    # UPDATE / UPLOAD FILES
    # --------------------------------------------------------

    volunteer = (
        Volunteer.query.get_or_404(
            volunteer_id
        )
    )

    photo = request.files.get(
        "photo"
    )

    signature = request.files.get(
        "signature"
    )

    if photo and photo.filename:

        photo_filename = (
            f"{volunteer.volunteer_id}_photo_{photo.filename}"
        )

        photo.save(
            os.path.join(
                app.config["VOLUNTEER_UPLOAD_FOLDER"],
                photo_filename
            )
        )

        volunteer.photo = photo_filename

    if signature and signature.filename:

        signature_filename = (
            f"{volunteer.volunteer_id}_signature_{signature.filename}"
        )

        signature.save(
            os.path.join(
                app.config["VOLUNTEER_UPLOAD_FOLDER"],
                signature_filename
            )
        )

        volunteer.signature = signature_filename

    db.session.commit()

    return redirect(
        url_for(
            "view_volunteer",
            volunteer_id=volunteer.id
        )
    )
# ============================================================
# VOLUNTEER - EDIT
# ============================================================

@app.route(
    "/admin/volunteers/<int:volunteer_id>/edit",
    methods=["GET", "POST"]
)
def edit_volunteer(volunteer_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    volunteer = (
        Volunteer.query.get_or_404(
            volunteer_id
        )
    )

    if request.method == "POST":

        volunteer.name = request.form.get(
            "name",
            ""
        ).strip()

        volunteer.father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        volunteer.dob = request.form.get(
            "dob",
            ""
        ).strip()

        volunteer.gender = request.form.get(
            "gender",
            ""
        ).strip()

        volunteer.mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        volunteer.email = request.form.get(
            "email",
            ""
        ).strip()

        volunteer.address = request.form.get(
            "address",
            ""
        ).strip()

        volunteer.village = request.form.get(
            "village",
            ""
        ).strip()

        volunteer.post = request.form.get(
            "post",
            ""
        ).strip()

        volunteer.police_station = request.form.get(
            "police_station",
            ""
        ).strip()

        volunteer.district = request.form.get(
            "district",
            ""
        ).strip()

        volunteer.state = request.form.get(
            "state",
            ""
        ).strip()

        volunteer.pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        volunteer.education = request.form.get(
            "education",
            ""
        ).strip()

        volunteer.occupation = request.form.get(
            "occupation",
            ""
        ).strip()

        volunteer.area = request.form.get(
            "area",
            ""
        ).strip()

        volunteer.volunteer_type = request.form.get(
            "volunteer_type",
            "General"
        ).strip()

        volunteer.joining_date = request.form.get(
            "joining_date",
            ""
        ).strip()

        volunteer.skills = request.form.get(
            "skills",
            ""
        ).strip()

        volunteer.status = request.form.get(
            "status",
            "Active"
        ).strip()

        photo = request.files.get(
            "photo"
        )

        signature = request.files.get(
            "signature"
        )

        if photo and photo.filename:

            photo_filename = (
                f"{volunteer.volunteer_id}_photo_{photo.filename}"
            )

            photo.save(
                os.path.join(
                    app.config["VOLUNTEER_UPLOAD_FOLDER"],
                    photo_filename
                )
            )

            volunteer.photo = photo_filename

        if signature and signature.filename:

            signature_filename = (
                f"{volunteer.volunteer_id}_signature_{signature.filename}"
            )

            signature.save(
                os.path.join(
                    app.config["VOLUNTEER_UPLOAD_FOLDER"],
                    signature_filename
                )
            )

            volunteer.signature = signature_filename

        db.session.commit()

        return redirect(
            url_for(
                "view_volunteer",
                volunteer_id=volunteer.id
            )
        )

    return render_template(
        "edit_volunteer.html",
        volunteer=volunteer
    )


# ============================================================
# VOLUNTEER - DELETE
# ============================================================

@app.route(
    "/admin/volunteers/<int:volunteer_id>/delete",
    methods=["POST"]
)
def delete_volunteer(volunteer_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    volunteer = (
        Volunteer.query.get_or_404(
            volunteer_id
        )
    )

    db.session.delete(volunteer)

    db.session.commit()

    return redirect(
        url_for("volunteers_list")
    )


# ============================================================
# DONATION - ADD
# ============================================================

@app.route(
    "/admin/donations/add",
    methods=["GET", "POST"]
)
def add_donation():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        from decimal import Decimal, InvalidOperation

        donation_date = request.form.get(
            "donation_date",
            ""
        ).strip()

        donation_type = request.form.get(
            "donation_type",
            "One Time"
        ).strip()

        donor_name = request.form.get(
            "donor_name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        pan = request.form.get(
            "pan",
            ""
        ).strip()

        amount_text = request.form.get(
            "amount",
            "0"
        ).strip()

        purpose = request.form.get(
            "purpose",
            ""
        ).strip()

        payment_mode = request.form.get(
            "payment_mode",
            ""
        ).strip()

        transaction_reference = (
            request.form.get(
                "transaction_reference",
                ""
            ).strip()
        )

        payment_status = request.form.get(
            "payment_status",
            "Received"
        ).strip()

        remarks = request.form.get(
            "remarks",
            ""
        ).strip()

        if not donor_name:

            return """
            <script>
                alert("Donor name is required");
                window.history.back();
            </script>
            """

        try:

            amount_text = amount_text.replace(
                ",",
                ""
            )

            amount = Decimal(
                amount_text
            ).quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            return """
            <script>
                alert("Please enter a valid donation amount");
                window.history.back();
            </script>
            """

        if amount <= 0:

            return """
            <script>
                alert("Donation amount must be greater than zero");
                window.history.back();
            </script>
            """

        last_donation = (
            Donation.query
            .order_by(
                Donation.id.desc()
            )
            .first()
        )

        if last_donation is None:
            next_number = 1
        else:
            next_number = (
                last_donation.id + 1
            )

        donation_id = (
            f"SJT-D-{next_number:05d}"
        )

        donation = Donation(

            donation_id=donation_id,

            donation_date=donation_date,

            donation_type=donation_type,

            donor_name=donor_name,

            mobile=mobile,

            email=email,

            address=address,

            pan=pan,

            amount=amount,

            purpose=purpose,

            payment_mode=payment_mode,

            transaction_reference=(
                transaction_reference
            ),

            payment_status=payment_status,

            remarks=remarks
        )

        db.session.add(donation)

        db.session.commit()

        return redirect(
            url_for(
                "view_donation",
                donation_id=donation.id
            )
        )

    return render_template(
        "add_donation.html"
    )
# ============================================================
# DONATION - LIST
# ============================================================

@app.route("/admin/donations")
def donations_list():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    search = request.args.get(
        "search",
        ""
    ).strip()

    payment_status = request.args.get(
        "payment_status",
        ""
    ).strip()

    query = Donation.query

    if search:

        query = query.filter(
            db.or_(
                Donation.donation_id.ilike(
                    f"%{search}%"
                ),
                Donation.donor_name.ilike(
                    f"%{search}%"
                ),
                Donation.mobile.ilike(
                    f"%{search}%"
                ),
                Donation.transaction_reference.ilike(
                    f"%{search}%"
                )
            )
        )

    if (
        payment_status
        and payment_status != "All"
    ):

        query = query.filter(
            Donation.payment_status
            == payment_status
        )

    donations = (
        query
        .order_by(
            Donation.id.desc()
        )
        .all()
    )

    total_amount = sum(
        donation.amount or 0
        for donation in donations
    )

    return render_template(
        "donations.html",

        donations=donations,

        search=search,

        payment_status=payment_status,

        total_amount=total_amount
    )


# ============================================================
# DONATION - VIEW
# ============================================================

@app.route(
    "/admin/donations/<int:donation_id>"
)
def view_donation(donation_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    donation = (
        Donation.query.get_or_404(
            donation_id
        )
    )

    return render_template(
        "view_donation.html",
        donation=donation
    )


# ============================================================
# DONATION - EDIT
# ============================================================

@app.route(
    "/admin/donations/<int:donation_id>/edit",
    methods=["GET", "POST"]
)
def edit_donation(donation_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    donation = (
        Donation.query.get_or_404(
            donation_id
        )
    )

    if request.method == "POST":

        from decimal import Decimal, InvalidOperation

        donation_date = request.form.get(
            "donation_date",
            ""
        ).strip()

        donation_type = request.form.get(
            "donation_type",
            "One Time"
        ).strip()

        donor_name = request.form.get(
            "donor_name",
            ""
        ).strip()

        mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        pan = request.form.get(
            "pan",
            ""
        ).strip()

        amount_text = request.form.get(
            "amount",
            "0"
        ).strip()

        purpose = request.form.get(
            "purpose",
            ""
        ).strip()

        payment_mode = request.form.get(
            "payment_mode",
            ""
        ).strip()

        transaction_reference = (
            request.form.get(
                "transaction_reference",
                ""
            ).strip()
        )

        payment_status = request.form.get(
            "payment_status",
            "Received"
        ).strip()

        remarks = request.form.get(
            "remarks",
            ""
        ).strip()

        if not donor_name:

            return """
            <script>
                alert("Donor name is required");
                window.history.back();
            </script>
            """

        try:

            amount_text = amount_text.replace(
                ",",
                ""
            )

            amount = Decimal(
                amount_text
            ).quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            return """
            <script>
                alert("Please enter a valid donation amount");
                window.history.back();
            </script>
            """

        if amount <= 0:

            return """
            <script>
                alert("Donation amount must be greater than zero");
                window.history.back();
            </script>
            """

        donation.donation_date = donation_date

        donation.donation_type = donation_type

        donation.donor_name = donor_name

        donation.mobile = mobile

        donation.email = email

        donation.address = address

        donation.pan = pan

        donation.amount = amount

        donation.purpose = purpose

        donation.payment_mode = payment_mode

        donation.transaction_reference = (
            transaction_reference
        )

        donation.payment_status = payment_status

        donation.remarks = remarks

        db.session.commit()

        return redirect(
            url_for(
                "view_donation",
                donation_id=donation.id
            )
        )

    return render_template(
        "edit_donation.html",
        donation=donation
    )


# ============================================================
# DONATION - DELETE
# ============================================================

@app.route(
    "/admin/donations/<int:donation_id>/delete",
    methods=["POST"]
)
def delete_donation(donation_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    donation = (
        Donation.query.get_or_404(
            donation_id
        )
    )

    db.session.delete(donation)

    db.session.commit()

    return redirect(
        url_for("donations_list")
    )


# ============================================================
# DONATION - RECEIPT
# ============================================================

@app.route(
    "/admin/donations/<int:donation_id>/receipt"
)
def donation_receipt(donation_id):

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    donation = (
        Donation.query.get_or_404(
            donation_id
        )
    )

    return render_template(
        "donation_receipt.html",
        donation=donation
    )


# ============================================================
# DONATION - SUMMARY
# ============================================================

@app.route(
    "/admin/donations/summary"
)
def donation_summary():

    if not session.get(
        "admin_logged_in"
    ):
        return redirect(
            url_for("admin_login")
        )

    total_donations = (
        Donation.query.count()
    )

    total_amount = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(
                    Donation.amount
                ),
                0
            )
        ).scalar()
        or 0
    )

    received_amount = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(
                    Donation.amount
                ),
                0
            )
        )
        .filter(
            Donation.payment_status
            == "Received"
        )
        .scalar()
        or 0
    )

    pending_amount = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(
                    Donation.amount
                ),
                0
            )
        )
        .filter(
            Donation.payment_status
            == "Pending"
        )
        .scalar()
        or 0
    )

    return render_template(
        "donation_summary.html",

        total_donations=total_donations,

        total_amount=total_amount,

        received_amount=received_amount,

        pending_amount=pending_amount
    )
# ============================================================
# DATABASE CREATE + SAFE EXISTING DATABASE MIGRATION
# ============================================================

with app.app_context():

    # --------------------------------------------------------
    # CREATE NEW TABLES
    # --------------------------------------------------------

    db.create_all()

    # --------------------------------------------------------
    # HELPER FUNCTION
    # --------------------------------------------------------

    def add_missing_columns(
        table_name,
        columns
    ):

        connection = db.engine.raw_connection()

        cursor = connection.cursor()

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        existing_columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        for column_name, column_definition in columns:

            if column_name not in existing_columns:

                cursor.execute(
                    f"ALTER TABLE {table_name} "
                    f"ADD COLUMN {column_name} "
                    f"{column_definition}"
                )

        connection.commit()

        cursor.close()

        connection.close()


    # ========================================================
    # MEMBER TABLE
    # ========================================================

    add_missing_columns(
        "member",
        [

            (
                "member_id",
                "VARCHAR(50) DEFAULT ''"
            ),

            (
                "name",
                "VARCHAR(100)"
            ),

            (
                "father_name",
                "VARCHAR(100)"
            ),

            (
                "dob",
                "VARCHAR(20)"
            ),

            (
                "gender",
                "VARCHAR(20)"
            ),

            (
                "mobile",
                "VARCHAR(20)"
            ),

            (
                "email",
                "VARCHAR(100)"
            ),

            (
                "address",
                "TEXT"
            ),

            (
                "village",
                "VARCHAR(100)"
            ),

            (
                "post",
                "VARCHAR(100)"
            ),

            (
                "police_station",
                "VARCHAR(100)"
            ),

            (
                "district",
                "VARCHAR(100)"
            ),

            (
                "state",
                "VARCHAR(100)"
            ),

            (
                "pincode",
                "VARCHAR(20)"
            ),

            (
                "id_proof_type",
                "VARCHAR(50)"
            ),

            (
                "id_proof_number",
                "VARCHAR(100)"
            ),

            (
                "occupation",
                "VARCHAR(100)"
            ),

            (
                "education",
                "VARCHAR(100)"
            ),

            (
                "membership_date",
                "VARCHAR(20)"
            ),

            (
                "status",
                "VARCHAR(30)"
            ),

            (
                "photo",
                "VARCHAR(255)"
            ),

            (
                "signature",
                "VARCHAR(255)"
            ),

            (
                "id_proof",
                "VARCHAR(255)"
            ),

            (
                "address_proof",
                "VARCHAR(255)"
            )
        ]
    )


    # ========================================================
    # VOLUNTEER TABLE
    # ========================================================

    add_missing_columns(
        "volunteer",
        [

            (
                "volunteer_id",
                "VARCHAR(50) DEFAULT ''"
            ),

            (
                "name",
                "VARCHAR(100)"
            ),

            (
                "father_name",
                "VARCHAR(100)"
            ),

            (
                "dob",
                "VARCHAR(20)"
            ),

            (
                "gender",
                "VARCHAR(20)"
            ),

            (
                "mobile",
                "VARCHAR(20)"
            ),

            (
                "email",
                "VARCHAR(100)"
            ),

            (
                "address",
                "TEXT"
            ),

            (
                "village",
                "VARCHAR(100)"
            ),

            (
                "post",
                "VARCHAR(100)"
            ),

            (
                "police_station",
                "VARCHAR(100)"
            ),

            (
                "district",
                "VARCHAR(100)"
            ),

            (
                "state",
                "VARCHAR(100)"
            ),

            (
                "pincode",
                "VARCHAR(20)"
            ),

            (
                "education",
                "VARCHAR(100)"
            ),

            (
                "occupation",
                "VARCHAR(100)"
            ),

            (
                "joining_date",
                "VARCHAR(20)"
            ),

            (
                "status",
                "VARCHAR(30)"
            ),

            (
                "photo",
                "VARCHAR(255)"
            ),

            (
                "signature",
                "VARCHAR(255)"
            )
        ]
    )


    # ========================================================
    # ASSISTANCE APPLICATION TABLE
    # ========================================================

    add_missing_columns(
        "assistance_application",
        [

            (
                "application_id",
                "VARCHAR(50) DEFAULT ''"
            ),

            (
                "application_no",
                "VARCHAR(50)"
            ),

            (
                "applicant_name",
                "VARCHAR(100)"
            ),

            (
                "father_name",
                "VARCHAR(100)"
            ),

            (
                "dob",
                "VARCHAR(20)"
            ),

            (
                "gender",
                "VARCHAR(20)"
            ),

            (
                "mobile",
                "VARCHAR(20)"
            ),

            (
                "email",
                "VARCHAR(100)"
            ),

            (
                "address",
                "TEXT"
            ),

            (
                "village",
                "VARCHAR(100)"
            ),

            (
                "post",
                "VARCHAR(100)"
            ),

            (
                "police_station",
                "VARCHAR(100)"
            ),

            (
                "district",
                "VARCHAR(100)"
            ),

            (
                "state",
                "VARCHAR(100)"
            ),

            (
                "pincode",
                "VARCHAR(20)"
            ),

            (
                "assistance_type",
                "VARCHAR(100)"
            ),

            (
                "assistance_amount",
                "VARCHAR(50)"
            ),

            (
                "reason",
                "TEXT"
            ),

            (
                "application_date",
                "VARCHAR(20)"
            ),

            (
                "status",
                "VARCHAR(30)"
            ),

            (
                "remarks",
                "TEXT"
            )
        ]
    )


    # ========================================================
    # DONATION TABLE
    # ========================================================

    add_missing_columns(
        "donation",
        [

            (
                "donation_id",
                "VARCHAR(30)"
            ),

            (
                "donation_date",
                "VARCHAR(20)"
            ),

            (
                "donation_type",
                "VARCHAR(30)"
            ),

            (
                "donor_name",
                "VARCHAR(150)"
            ),

            (
                "mobile",
                "VARCHAR(20)"
            ),

            (
                "email",
                "VARCHAR(150)"
            ),

            (
                "address",
                "TEXT"
            ),

            (
                "pan",
                "VARCHAR(30)"
            ),

            (
                "amount",
                "NUMERIC(12,2)"
            ),

            (
                "purpose",
                "VARCHAR(200)"
            ),

            (
                "payment_mode",
                "VARCHAR(50)"
            ),

            (
                "transaction_reference",
                "VARCHAR(150)"
            ),

            (
                "payment_status",
                "VARCHAR(30)"
            ),

            (
                "remarks",
                "TEXT"
            )
        ]
    )


    # ========================================================
    # PROGRAM / EVENT TABLE
    # ========================================================

    add_missing_columns(
        "program",
        [

            (
                "program_id",
                "VARCHAR(30)"
            ),

            (
                "title",
                "VARCHAR(200)"
            ),

            (
                "program_type",
                "VARCHAR(50)"
            ),

            (
                "program_date",
                "VARCHAR(20)"
            ),

            (
                "start_time",
                "VARCHAR(20)"
            ),

            (
                "end_time",
                "VARCHAR(20)"
            ),

            (
                "venue",
                "VARCHAR(200)"
            ),

            (
                "description",
                "TEXT"
            ),

            (
                "status",
                "VARCHAR(30)"
            ),

            (
                "remarks",
                "TEXT"
            )
        ]
    )
    # ========================================================
    # BACKFILL MEMBER IDs
    # ========================================================

    connection = db.engine.raw_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM member
        WHERE member_id IS NULL
           OR TRIM(member_id) = ''
        ORDER BY id
        """
    )

    member_rows = cursor.fetchall()

    for row in member_rows:

        member_database_id = row[0]

        generated_member_id = (
            f"SJT-M-{member_database_id:05d}"
        )

        cursor.execute(
            """
            UPDATE member
            SET member_id = ?
            WHERE id = ?
            """,
            (
                generated_member_id,
                member_database_id
            )
        )


    # ========================================================
    # BACKFILL VOLUNTEER IDs
    # ========================================================

    cursor.execute(
        """
        SELECT id
        FROM volunteer
        WHERE volunteer_id IS NULL
           OR TRIM(volunteer_id) = ''
        ORDER BY id
        """
    )

    volunteer_rows = cursor.fetchall()

    for row in volunteer_rows:

        volunteer_database_id = row[0]

        generated_volunteer_id = (
            f"SJT-V-{volunteer_database_id:05d}"
        )

        cursor.execute(
            """
            UPDATE volunteer
            SET volunteer_id = ?
            WHERE id = ?
            """,
            (
                generated_volunteer_id,
                volunteer_database_id
            )
        )


    # ========================================================
    # BACKFILL ASSISTANCE APPLICATION IDs
    # ========================================================

    cursor.execute(
        """
        SELECT id
        FROM assistance_application
        WHERE application_id IS NULL
           OR TRIM(application_id) = ''
        ORDER BY id
        """
    )

    application_rows = cursor.fetchall()

    for row in application_rows:

        application_database_id = row[0]

        generated_application_id = (
            f"SJT-A-{application_database_id:05d}"
        )

        cursor.execute(
            """
            UPDATE assistance_application
            SET application_id = ?
            WHERE id = ?
            """,
            (
                generated_application_id,
                application_database_id
            )
        )


    # ========================================================
    # KEEP APPLICATION_NO IN SYNC
    # ========================================================

    cursor.execute(
        """
        UPDATE assistance_application
        SET application_no = application_id
        WHERE (
            application_no IS NULL
            OR TRIM(application_no) = ''
        )
        AND application_id IS NOT NULL
        AND TRIM(application_id) != ''
        """
    )


    # ========================================================
    # BACKFILL PROGRAM IDs
    # ========================================================

    cursor.execute(
        """
        SELECT id
        FROM program
        WHERE program_id IS NULL
           OR TRIM(program_id) = ''
        ORDER BY id
        """
    )

    program_rows = cursor.fetchall()

    for row in program_rows:

        program_database_id = row[0]

        generated_program_id = (
            f"PRG-{program_database_id:03d}"
        )

        cursor.execute(
            """
            UPDATE program
            SET program_id = ?
            WHERE id = ?
            """,
            (
                generated_program_id,
                program_database_id
            )
        )


    # ========================================================
    # SAFE DONATION AMOUNT ROUNDING
    # ========================================================

    cursor.execute(
        """
        UPDATE donation
        SET amount = ROUND(amount, 2)
        WHERE amount IS NOT NULL
        """
    )


    # ========================================================
    # COMMIT ALL MIGRATION CHANGES
    # ========================================================

    connection.commit()

    cursor.close()

    connection.close()


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )