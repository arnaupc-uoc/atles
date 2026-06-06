from email.message import EmailMessage
import smtplib
import ssl
from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app import db
from app.models.user import User
from app.models.access_log import AccessLog
import subprocess
import os
import gzip
import csv
from io import StringIO
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


def current_role():
    if hasattr(current_user, "role") and current_user.role:
        return current_user.role
    if current_user.is_authenticated and current_user.username == "admin":
        return "admin"
    return "editor"


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("admin.login", next=request.path))
            if current_role() not in roles:
                flash("No tens permisos per accedir a aquesta pàgina.", "warning")
                return redirect(url_for("admin.home"))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_serializer():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt=current_app.config.get("SECURITY_PASSWORD_SALT", "dev_password_salt"),
    )


def generate_reset_token(email):
    serializer = get_serializer()
    return serializer.dumps(email)


def verify_reset_token(token, expiration=3600):
    serializer = get_serializer()
    return serializer.loads(token, max_age=expiration)


def send_reset_email(user):
    token = generate_reset_token(user.email)
    reset_url = url_for("admin.reset_password", token=token, _external=True)

    message = EmailMessage()
    message["Subject"] = "Recuperació de contrasenya Atles"
    message["From"] = current_app.config.get("MAIL_DEFAULT_SENDER")
    message["To"] = user.email
    message.set_content(
        f"""Hola {user.username},

Has sol·licitat restablir la teva contrasenya per a l'eina d'administració Atles.

Fes clic a l'enllaç següent per restablir la contrasenya:

{reset_url}

Aquest enllaç caduca en 1 hora.

Si no has sol·licitat aquesta acció, ignora aquest missatge.

Salutacions,
Atles
"""
    )

    mail_server = current_app.config.get("MAIL_SERVER", "localhost")
    mail_port = current_app.config.get("MAIL_PORT", 25)
    mail_username = current_app.config.get("MAIL_USERNAME")
    mail_password = current_app.config.get("MAIL_PASSWORD")
    use_tls = current_app.config.get("MAIL_USE_TLS", False)
    use_ssl = current_app.config.get("MAIL_USE_SSL", False)

    try:
        if use_ssl:
            smtp = smtplib.SMTP_SSL(mail_server, mail_port, context=ssl.create_default_context())
        else:
            smtp = smtplib.SMTP(mail_server, mail_port, timeout=10)
            if use_tls:
                smtp.starttls(context=ssl.create_default_context())

        with smtp as server:
            if mail_username and mail_password:
                server.login(mail_username, mail_password)
            server.send_message(message)

    except Exception as exc:
        current_app.logger.exception("Error enviant el correu de recuperació de contrasenya")
        raise RuntimeError("No s'ha pogut enviar el correu de recuperació. Intenta-ho més tard.")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.home"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        ip = request.remote_addr
        success = False
        if user and user.check_password(password):
            login_user(user)
            success = True
            next_page = request.args.get("next") or url_for("admin.home")
        else:
            error = "Usuari o contrasenya incorrectes."

        # Registrem l'intent d'accés
        try:
            log = AccessLog(
                user_id=(user.id if user else None),
                username=(user.username if user else username),
                ip=ip,
                action="login",
                success=success,
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            current_app.logger.exception("No s'ha pogut registrar l'access log")

        if success:
            return redirect(next_page)

    return render_template("login.html", error=error)


@admin_bp.route("/recover-password", methods=["GET", "POST"])
def recover_password():
    if current_user.is_authenticated:
        return redirect(url_for("admin.home"))

    message = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                try:
                    send_reset_email(user)
                    flash(
                        "Si us plau, revisa el teu correu per restablir la contrasenya.",
                        "info",
                    )
                except RuntimeError:
                    flash(
                        "No s'ha pogut enviar el correu de recuperació. Intenta-ho més tard.",
                        "error",
                    )
            else:
                current_app.logger.info(
                    "Password recovery requested for unknown email: %s", email
                )
                flash(
                    "Si l'adreça de correu existeix al nostre sistema, rebràs instruccions en breu.",
                    "info",
                )
            return redirect(url_for("admin.login"))
        message = "Introdueix una adreça de correu electrònic vàlida."

    return render_template("recover_password.html", message=message)


@admin_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("admin.home"))

    try:
        email = verify_reset_token(token)
    except SignatureExpired:
        flash("L'enllaç ha caducat. Torna a sol·licitar la recuperació.", "warning")
        return redirect(url_for("admin.recover_password"))
    except BadSignature:
        flash("L'enllaç de restabliment no és vàlid.", "error")
        return redirect(url_for("admin.recover_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Usuari no trobat per aquesta adreça.", "error")
        return redirect(url_for("admin.recover_password"))

    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not password:
            error = "Introdueix una nova contrasenya."
        elif password != confirm:
            error = "Les contrasenyes no coincideixen."
        else:
            user.set_password(password)
            db.session.commit()
            flash("Contrasenya actualitzada. Ara pots iniciar sessió.", "info")
            return redirect(url_for("admin.login"))

    return render_template(
        "reset_password.html",
        error=error,
        token=token,
    )


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def home():
    role = current_role()
    sections = [
        {
            "title": "Usuaris",
            "path": "/users",
            "description": "Gestió d'usuaris i permisos",
            "roles": ["admin"]
        },
        {
            "title": "Publicacions",
            "path": "/publications",
            "description": "Gestió de contingut i publicacions",
            "roles": ["admin", "editor"]
        },
        {
            "title": "Regions",
            "path": "/regions",
            "description": "Gestió de regions geogràfiques i mapes",
            "roles": ["admin", "editor"]
        }
    ]
    # Afegim autors i pàgines a les seccions de l'administració
    sections.extend([
        {
            "title": "Autors",
            "path": "/authors",
            "description": "Gestió d'autors i informació relacionada",
            "roles": ["admin", "editor"],
        },
        {
            "title": "Pàgines",
            "path": "/pages",
            "description": "Gestió de pàgines i contingut estàtic",
            "roles": ["admin", "editor"],
        },
    ])
    # Afegim la secció d'eines (nom en català: Eines)
    sections.append(
        {
            "title": "Eines",
            "path": "/tools",
            "description": "Utilitats i eines d'administració",
            "roles": ["admin"],
        }
    )
    visible_sections = [section for section in sections if role in section["roles"]]
    return render_template(
        "admin_home.html",
        user=current_user,
        role=role,
        sections=visible_sections,
    )


@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():
    return render_template(
        "admin_section.html",
        title="Usuaris",
        description="Gestió d'usuaris i permisos",
    )


@admin_bp.route("/publications")
@login_required
@role_required("admin", "editor")
def publications():
    return render_template(
        "admin_section.html",
        title="Publicacions",
        description="Gestió de publicacions i contingut relacionat.",
    )


@admin_bp.route("/regions")
@login_required
@role_required("admin", "editor")
def regions():
    return render_template(
        "admin_section.html",
        title="Regions",
        description="Gestió de regions i mapes geogràfics.",
    )


@admin_bp.route("/authors")
@login_required
@role_required("admin", "editor")
def authors():
    return render_template(
        "admin_section.html",
        title="Autors",
        description="Gestió d'autors i informació relacionada.",
    )


@admin_bp.route("/pages")
@login_required
@role_required("admin", "editor")
def pages():
    return render_template(
        "admin_section.html",
        title="Pàgines",
        description="Gestió de pàgines i contingut estàtic.",
    )


@admin_bp.route("/tools")
@login_required
@role_required("admin")
def tools():
    return render_template(
        "admin_tools.html",
        title="Eines",
        description="Eines i utilitats per a administradors",
    )


@admin_bp.route("/tools/backups")
@login_required
@role_required("admin")
def tools_backups():
    backups_dir = current_app.config.get("BACKUPS_DIR")
    files = []
    try:
        for fname in sorted(os.listdir(backups_dir), reverse=True):
            path = os.path.join(backups_dir, fname)
            if os.path.isfile(path):
                stat = os.stat(path)
                files.append({
                    "name": fname,
                    "size": stat.st_size,
                    "mtime": datetime.fromtimestamp(stat.st_mtime),
                })
    except Exception:
        current_app.logger.exception("Error llegint backups")

    return render_template(
        "admin_backups.html",
        title="Backups",
        description="Gestió de còpies de seguretat i restauració",
        files=files,
    )


@admin_bp.route("/tools/backups/create", methods=["POST"])
@login_required
@role_required("admin")
def tools_backups_create():
    backups_dir = current_app.config.get("BACKUPS_DIR")
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_name = f"backup_{timestamp}.sql.gz"
    out_path = os.path.join(backups_dir, out_name)

    db_url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    pg_dump = current_app.config.get("PG_DUMP_PATH", "pg_dump")

    try:
        # Use pg_dump with DATABASE_URL
        cmd = [pg_dump, db_url]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=300)
        if proc.returncode != 0:
            current_app.logger.error("pg_dump failed: %s", stderr.decode(errors='ignore'))
            flash("No s'ha pogut crear el backup.", "error")
            return redirect(url_for("admin.tools_backups"))

        with gzip.open(out_path, "wb") as f:
            f.write(stdout)

        flash("Backup creat correctament.", "info")
    except Exception:
        current_app.logger.exception("Error creant backup")
        flash("Error creant el backup.", "error")

    return redirect(url_for("admin.tools_backups"))


@admin_bp.route("/tools/backups/download/<filename>")
@login_required
@role_required("admin")
def tools_backups_download(filename):
    from flask import send_from_directory

    backups_dir = current_app.config.get("BACKUPS_DIR")
    return send_from_directory(backups_dir, filename, as_attachment=True)


@admin_bp.route("/tools/backups/restore", methods=["POST"])
@login_required
@role_required("admin")
def tools_backups_restore():
    backups_dir = current_app.config.get("BACKUPS_DIR")
    filename = request.form.get("filename")
    if not filename:
        flash("No has seleccionat cap backup.", "error")
        return redirect(url_for("admin.tools_backups"))

    path = os.path.join(backups_dir, filename)
    if not os.path.exists(path):
        flash("Backup no trobat.", "error")
        return redirect(url_for("admin.tools_backups"))

    psql = current_app.config.get("PSQL_PATH", "psql")
    db_url = current_app.config.get("SQLALCHEMY_DATABASE_URI")

    try:
        # Decompress and pipe to psql
        with gzip.open(path, "rb") as f:
            proc = subprocess.Popen([psql, db_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate(input=f.read(), timeout=600)
            if proc.returncode != 0:
                current_app.logger.error("psql restore failed: %s", stderr.decode(errors='ignore'))
                flash("Error restauran el backup.", "error")
                return redirect(url_for("admin.tools_backups"))

        flash("Backup restaurat correctament.", "info")
    except Exception:
        current_app.logger.exception("Error restauran backup")
        flash("Error restauran el backup.", "error")

    return redirect(url_for("admin.tools_backups"))


@admin_bp.route("/tools/accessos")
@login_required
@role_required("admin")
def tools_accessos():
    # Filtres
    q = AccessLog.query
    username = request.args.get("username")
    success = request.args.get("success")
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    if username:
        q = q.filter(AccessLog.username.ilike(f"%{username}%"))
    if success in ("1", "0"):
        q = q.filter(AccessLog.success == (success == "1"))
    if date_from:
        try:
            dt = datetime.fromisoformat(date_from)
            q = q.filter(AccessLog.created_at >= dt)
        except Exception:
            pass
    if date_to:
        try:
            dt = datetime.fromisoformat(date_to)
            q = q.filter(AccessLog.created_at <= dt)
        except Exception:
            pass

    q = q.order_by(AccessLog.created_at.desc())

    # Export CSV
    if request.args.get("export") == "csv":
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(["id", "username", "ip", "action", "success", "created_at"])
        for row in q.limit(1000).all():
            writer.writerow([row.id, row.username, row.ip, row.action, row.success, row.created_at.isoformat()])
        return current_app.response_class(si.getvalue(), mimetype="text/csv")

    entries = q.limit(500).all()
    return render_template(
        "admin_accessos.html",
        title="Accessos usuaris",
        description="Registre d'accessos d'usuaris i controls d'auditoria",
        entries=entries,
    )


@admin_bp.route("/tools/logs")
@login_required
@role_required("admin")
def tools_logs():
    log_file = current_app.config.get("LOG_FILE")
    tail = []
    try:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                tail = lines[-500:]
    except Exception:
        current_app.logger.exception("Error llegint log file")

    # Export
    if request.args.get("export") == "csv":
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(["line"])
        for line in tail:
            writer.writerow([line.strip()])
        return current_app.response_class(si.getvalue(), mimetype="text/csv")

    return render_template(
        "admin_logs.html",
        title="Logs",
        description="Visualització i exportació de logs del sistema",
        tail=tail,
    )
